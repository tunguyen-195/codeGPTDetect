"""
T07GPTcodeDetect Multi-Language API Server
Supports: Java, Python (C++ ready)
"""

import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from multilang_detector import get_detector


class PredictRequest(BaseModel):
    code: str
    language: Optional[str] = None  # 'java', 'python', or None for auto-detect
    model: Optional[str] = None  # 'base', 'java', 'python', or None for auto-select


class MultiLangDetectorService:
    def __init__(self):
        self.detector = get_detector()
        print("\n" + "="*70)
        print("MULTI-LANGUAGE DETECTION SERVICE STARTED")
        print("="*70)
        print(f"Supported Languages: {', '.join(self.detector.get_supported_languages()).upper()}")
        print("="*70 + "\n")
    
    def predict(self, code: str, language: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Predict with multi-language and multi-model support"""
        try:
            return self.detector.predict(code, language=language, model=model)
        except Exception as e:
            return {
                "error": str(e),
                "supported_languages": self.detector.get_supported_languages(),
                "available_models": list(self.detector.models.keys())
            }
    
    def get_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "service": "T07GPTcodeDetect Multi-Language Detector",
            "version": "2.0.0",
            "supported_languages": self.detector.get_supported_languages(),
            "available_models": list(self.detector.models.keys()),
            "model_descriptions": self.detector.model_descriptions,
            "features": [
                "Auto language detection",
                "Multiple model selection (Base/Java/Python)",
                "Java code detection",
                "Python code detection",
                "C++ ready (model not loaded)"
            ]
        }


# Initialize service
service = MultiLangDetectorService()

# Create FastAPI app
app = FastAPI(
    title="T07GPTcodeDetect Multi-Language API",
    version="2.0.0",
    description="AI-generated code detection for multiple programming languages"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def api_root() -> Dict[str, str]:
    """API root endpoint"""
    return {
        "message": "T07GPTcodeDetect Multi-Language API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "ok",
        **service.get_info()
    }


@app.get("/languages")
def get_languages() -> Dict[str, Any]:
    """Get supported languages"""
    return {
        "supported_languages": service.detector.get_supported_languages(),
        "count": len(service.detector.get_supported_languages())
    }


@app.get("/models")
def get_models() -> Dict[str, Any]:
    """Get available models"""
    return {
        "available_models": list(service.detector.models.keys()),
        "model_descriptions": service.detector.model_descriptions,
        "count": len(service.detector.models)
    }


@app.post("/predict")
def predict_json(payload: PredictRequest) -> Dict[str, Any]:
    """
    Predict if code is AI-generated or human-written
    
    Request body:
        - code: Source code to analyze (required)
        - language: Programming language ('java', 'python', or null for auto-detect)
        - model: Model to use ('base', 'java', 'python', or null for auto-select)
    
    Returns:
        - label: "AI-Generated" or "Human-Written"
        - confidence: Confidence score (0-1)
        - probabilities: Individual class probabilities
        - language: Detected/specified language
        - auto_detected: Whether language was auto-detected
        - model_used: Which model was used
        - model_description: Description of the model
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Missing field 'code'")
    
    try:
        result = service.predict(payload.code, payload.language, payload.model)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/predict-file")
async def predict_file(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    encoding: str = Form("utf-8")
) -> Dict[str, Any]:
    """
    Predict from uploaded file
    
    Form parameters:
        - file: Code file to analyze (required)
        - language: Programming language (optional, auto-detect if not provided)
        - model: Model to use (optional, auto-select if not provided)
        - encoding: File encoding (default: utf-8)
    """
    try:
        raw_bytes = await file.read()
        code = raw_bytes.decode(encoding, errors="ignore")
        
        result = service.predict(code, language, model)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Add filename to result
        result["filename"] = file.filename
        
        return result
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/detect-language")
def detect_language(payload: PredictRequest) -> Dict[str, Any]:
    """
    Detect programming language from code
    
    Request body:
        - code: Source code to analyze
    
    Returns:
        - language: Detected language
        - supported: Whether the language is supported
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Missing field 'code'")
    
    try:
        language = service.detector.detect_language(payload.code)
        is_supported = service.detector.is_language_supported(language)
        
        return {
            "language": language.upper(),
            "supported": is_supported,
            "available_models": service.detector.get_supported_languages()
        }
        
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# Serve static UI at root
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.isdir(static_dir):
    # Mount at both /ui and / (root will be last, acts as fallback)
    from starlette.responses import FileResponse
    
    @app.get("/")
    async def serve_root():
        """Serve index.html at root"""
        return FileResponse(os.path.join(static_dir, "index.html"))
    
    app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("STARTING GPTSNIFFER MULTI-LANGUAGE API SERVER")
    print("="*70)
    print("Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("UI: http://localhost:8000/ui")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
