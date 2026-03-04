import os
from typing import Optional, Dict, Any

import torch
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from starlette.staticfiles import StaticFiles


class PredictRequest(BaseModel):
    code: str


class DetectorService:
    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Get project root directory (parent of webapp/server)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        default_model_path = os.path.join(project_root, "models", "java-detector-finetuned")
        self.model_dir_finetuned: str = os.getenv("MODEL_DIR", default_model_path)
        self.model_name_base = os.getenv("MODEL_NAME", "microsoft/codebert-base")
        self.labels = {0: "ChatGPT", 1: "Human"}
        self.model = None
        self.tokenizer = None
        self.model_source = ""
        self.use_finetuned = False
        self._load_model(use_finetuned=False)

    def _load_model(self, use_finetuned: bool = False) -> None:
        try:
            if use_finetuned and os.path.isdir(self.model_dir_finetuned):
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir_finetuned)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_dir_finetuned)
                self.model_source = f"Fine-tuned: {os.path.basename(self.model_dir_finetuned)}"
                self.use_finetuned = True
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_base)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name_base)
                self.model_source = f"Base: {self.model_name_base}"
                self.use_finetuned = False

            self.model.to(self.device)
            self.model.eval()
        except Exception as exc:
            raise RuntimeError(f"Failed to load model/tokenizer: {exc}")

    def switch_model(self, use_finetuned: bool) -> Dict[str, str]:
        try:
            self._load_model(use_finetuned=use_finetuned)
            return {
                "status": "success",
                "model": self.model_source,
                "is_finetuned": self.use_finetuned
            }
        except Exception as exc:
            return {
                "status": "error",
                "message": str(exc),
                "model": self.model_source,
                "is_finetuned": self.use_finetuned
            }

    @torch.inference_mode()
    def predict(self, code: str, max_length: int = 512) -> Dict[str, Any]:
        if not code or not code.strip():
            raise ValueError("Empty code input")

        inputs = self.tokenizer(
            code,
            padding="max_length",
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model(**inputs)
        logits = outputs.logits.detach().cpu()
        probs = torch.softmax(logits, dim=-1).squeeze(0)
        conf_values = probs.tolist()

        if len(conf_values) < 2:
            # Ensure two-class output even for unfine-tuned heads
            conf_values = conf_values + [0.0] * (2 - len(conf_values))

        best_idx = int(torch.argmax(probs).item()) if probs.numel() > 0 else 0
        label = self.labels.get(best_idx, str(best_idx))

        return {
            "label": label,
            "confidence": float(conf_values[best_idx]) if conf_values else 0.0,
            "probabilities": {
                self.labels.get(0, "0"): float(conf_values[0]) if len(conf_values) > 0 else 0.0,
                self.labels.get(1, "1"): float(conf_values[1]) if len(conf_values) > 1 else 0.0,
            },
            "model_source": self.model_source,
            "device": str(self.device),
        }


service = DetectorService()

app = FastAPI(title="T07GPTcodeDetect Web API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok", 
        "model": service.model_source,
        "is_finetuned": service.use_finetuned
    }


@app.post("/predict")
def predict_json(payload: Optional[PredictRequest] = None) -> Dict[str, Any]:
    if payload is None or not payload.code:
        raise HTTPException(status_code=400, detail="Missing field 'code'")
    try:
        return service.predict(payload.code)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...), encoding: str = Form("utf-8")) -> Dict[str, Any]:
    try:
        raw_bytes = await file.read()
        code = raw_bytes.decode(encoding, errors="ignore")
        return service.predict(code)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/switch-model")
def switch_model(use_finetuned: bool) -> Dict[str, Any]:
    return service.switch_model(use_finetuned)


# Serve static UI
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


