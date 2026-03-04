# KẾ HOẠCH THỰC HIỆN MODULE 5: HỖ TRỢ ĐA NGÔN NGỮ LẬP TRÌNH

## 📋 TỔNG QUAN

**Mục tiêu:** Mở rộng hệ thống từ chỉ Java sang Python và C++ để phát hiện AI-generated code

**Timeline:** 4-6 tuần

**Ngôn ngữ ưu tiên:**
1. ✅ Java (đã có)
2. 🔥 Python (Priority 1)
3. 🔥 C++ (Priority 2)

---

## 🎯 GIAI ĐOẠN 1: THU THẬP DATASET (Tuần 1-2)

### A. PYTHON DATASET

#### 1. Human-written Code Sources

**Source 1: HuggingFace CodeSearchNet (CHÍNH)**
```
Dataset: code-search-net/code_search_net
Language: Python
Size: ~450K functions
URL: https://huggingface.co/datasets/code-search-net/code_search_net
```

**Download command:**
```python
from datasets import load_dataset

# Load Python subset
ds = load_dataset("code-search-net/code_search_net", "python")

# Statistics:
# - train: ~412K samples
# - validation: ~23K samples  
# - test: ~22K samples
```

**Source 2: OpenAI HumanEval**
```
Dataset: openai/human-eval
Size: 164 hand-crafted problems
URL: https://github.com/openai/human-eval
Use: Testing quality, not training
```

**Source 3: LeetCode Solutions**
```
Dataset: LeetCode-in-Python (community solutions)
Size: 2000+ problems
URL: GitHub repositories
Quality: High (human-reviewed)
```

**Source 4: Python Educational Code**
```
Dataset: Microsoft PythonProgrammingPuzzles
URL: https://github.com/microsoft/PythonProgrammingPuzzles
Size: 200+ puzzles with solutions
Quality: Very high (manually curated)
```

#### 2. AI-generated Code Collection

**Method 1: ChatGPT Prompts (Tự tạo)**
```
Cần tạo: 2000 samples
Approach:
- Sử dụng ChatGPT API (hoặc web interface)
- Prompts từ:
  * LeetCode problems
  * HackerRank challenges
  * Real assignment topics
  
Categories:
- Data structures (Arrays, Lists, Trees, Graphs)
- Algorithms (Sorting, Searching, DP)
- OOP concepts
- File handling
- Web scraping basics
```

**Prompt Template:**
```
User: Write a Python function to [TASK DESCRIPTION].
The function should:
- Have proper docstrings
- Include error handling
- Be well-commented
- Follow PEP 8 style guide

Example tasks:
1. "find the longest palindrome substring in a string"
2. "implement a binary search tree with insert and delete"
3. "calculate factorial using recursion"
```

**Method 2: Synthetic Generation**
```
Use existing AI code generators:
- GitHub Copilot outputs (nếu có access)
- Claude Code generations
- Gemini Code generations
```

---

### B. C++ DATASET

#### 1. Human-written Code Sources

**Source 1: Competitive Programming Archives**
```
Repositories:
- LeetCode-in-Cpp: https://github.com/leetcode-in-cpp/leetcode-in-cpp
  Size: 2000+ problems
  
- AlgoStruct: https://github.com/merteldem1r/algostruct
  Size: 100+ algorithms & data structures
  
- DSA-ICPC-Library: https://github.com/yiqiwang128/dsa-icpc-library
  Size: Comprehensive DSA collection
```

**Source 2: CodeSearchNet C++ (if available)**
```
from datasets import load_dataset
ds = load_dataset("code-search-net/code_search_net", "cpp")
```

**Source 3: GitHub C++ Projects**
```
Mining repositories:
- Algorithm implementations
- Data structure libraries
- Educational projects
```

#### 2. AI-generated C++ Code

**Similar approach to Python:**
```
Cần tạo: 1500 samples

Prompt focus:
- STL usage (vector, map, set)
- Pointer manipulation
- Memory management
- Template programming
- Algorithm implementations
```

**Prompt Template:**
```
User: Write a C++ program to [TASK].
Requirements:
- Use STL where appropriate
- Include proper memory management
- Add comments explaining logic
- Handle edge cases

Example tasks:
1. "implement a AVL tree with rotation operations"
2. "solve the 0-1 knapsack problem using dynamic programming"
3. "implement Dijkstra's shortest path algorithm"
```

---

## 🎯 GIAI ĐOẠN 2: XỬ LÝ & CHUẨN BỊ DATASET (Tuần 2)

### A. Dataset Structure

```
DATASETS/
├── PYTHON/
│   ├── training_data/
│   │   ├── 0_chatgpt_sample001.py    # AI-generated
│   │   ├── 0_chatgpt_sample002.py
│   │   ├── 1_human_sample001.py      # Human-written
│   │   ├── 1_human_sample002.py
│   │   └── ...
│   └── testing_data/
│       ├── 0_chatgpt_test001.py
│       ├── 1_human_test001.py
│       └── ...
│
└── CPP/
    ├── training_data/
    │   ├── 0_chatgpt_sample001.cpp
    │   ├── 1_human_sample001.cpp
    │   └── ...
    └── testing_data/
        └── ...
```

### B. Data Preprocessing Script

**File: `scripts/prepare_multilang_dataset.py`**

```python
import os
import json
from pathlib import Path
from datasets import load_dataset
import random
from tqdm import tqdm

class MultiLangDatasetPreparer:
    def __init__(self, output_dir="./DATASETS"):
        self.output_dir = Path(output_dir)
        
    def download_python_dataset(self):
        """Download and process CodeSearchNet Python"""
        print("Downloading CodeSearchNet Python...")
        ds = load_dataset("code-search-net/code_search_net", "python", 
                         split="train")
        
        # Sample 2000 human-written examples
        samples = ds.shuffle(seed=42).select(range(2000))
        
        output_dir = self.output_dir / "PYTHON" / "raw" / "human"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, sample in enumerate(tqdm(samples)):
            # Extract function code
            code = sample['func_code_string']
            
            # Save with label 1 (human)
            filename = f"1_human_{idx:04d}.py"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
        
        print(f"Saved {len(samples)} human Python samples")
        
    def download_cpp_dataset(self):
        """Download C++ from various sources"""
        # TODO: Implement C++ collection from GitHub repos
        pass
        
    def generate_ai_samples_python(self, num_samples=2000):
        """Generate AI samples using prompts"""
        # This will be manual or semi-automated
        print(f"Need to generate {num_samples} AI Python samples")
        print("Use ChatGPT API or manual prompting")
        
    def split_train_test(self, language="python", train_ratio=0.8):
        """Split into training and testing sets"""
        raw_dir = self.output_dir / language.upper() / "raw"
        train_dir = self.output_dir / language.upper() / "training_data"
        test_dir = self.output_dir / language.upper() / "testing_data"
        
        train_dir.mkdir(parents=True, exist_ok=True)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Get all files
        human_files = list((raw_dir / "human").glob("*.py" if language == "python" else "*.cpp"))
        ai_files = list((raw_dir / "ai").glob("*.py" if language == "python" else "*.cpp"))
        
        # Shuffle
        random.shuffle(human_files)
        random.shuffle(ai_files)
        
        # Split
        human_split = int(len(human_files) * train_ratio)
        ai_split = int(len(ai_files) * train_ratio)
        
        # Copy to train
        for f in human_files[:human_split]:
            shutil.copy(f, train_dir / f.name)
        for f in ai_files[:ai_split]:
            shutil.copy(f, train_dir / f.name)
            
        # Copy to test
        for f in human_files[human_split:]:
            shutil.copy(f, test_dir / f.name)
        for f in ai_files[ai_split:]:
            shutil.copy(f, test_dir / f.name)
        
        print(f"Split complete: {len(human_files[:human_split]) + len(ai_files[:ai_split])} train, "
              f"{len(human_files[human_split:]) + len(ai_files[ai_split:])} test")

if __name__ == "__main__":
    preparer = MultiLangDatasetPreparer()
    
    # Step 1: Download human-written code
    preparer.download_python_dataset()
    # preparer.download_cpp_dataset()
    
    # Step 2: Generate AI samples (manual/semi-auto)
    # preparer.generate_ai_samples_python()
    
    # Step 3: Split train/test
    # preparer.split_train_test("python")
```

---

## 🎯 GIAI ĐOẠN 3: FINE-TUNING MODELS (Tuần 3-4)

### A. Training Script for Python

**File: `train_python_model.py`**

```python
import os
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np

class PythonCodeDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.files = []
        self.labels = []
        
        # Load all files
        for filename in os.listdir(data_dir):
            if filename.endswith('.py'):
                filepath = os.path.join(data_dir, filename)
                label = int(filename.split('_')[0])  # 0=AI, 1=Human
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                self.files.append(code)
                self.labels.append(label)
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        code = self.files[idx]
        label = self.labels[idx]
        
        # Tokenize
        encoding = self.tokenizer(
            code,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary'
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_python_model():
    # Configuration
    MODEL_NAME = "microsoft/codebert-base"
    TRAIN_DIR = "./DATASETS/PYTHON/training_data"
    TEST_DIR = "./DATASETS/PYTHON/testing_data"
    OUTPUT_DIR = "./models/codebert-python-v1"
    
    # Load tokenizer and model
    print("Loading CodeBERT...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )
    
    # Prepare datasets
    print("Preparing datasets...")
    train_dataset = PythonCodeDataset(TRAIN_DIR, tokenizer)
    test_dataset = PythonCodeDataset(TEST_DIR, tokenizer)
    
    print(f"Train samples: {len(train_dataset)}")
    print(f"Test samples: {len(test_dataset)}")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=12,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=5e-5,
        weight_decay=0.01,
        warmup_steps=500,
        logging_dir=f'{OUTPUT_DIR}/logs',
        logging_steps=100,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        report_to="none"
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Evaluate
    print("\nEvaluating on test set...")
    results = trainer.evaluate()
    print(results)
    
    # Save final model
    print(f"\nSaving model to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("Training complete!")
    
    return results

if __name__ == "__main__":
    results = train_python_model()
```

### B. Training Script for C++

**Similar to Python, adjust:**
```python
# In train_cpp_model.py
class CppCodeDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, tokenizer, max_length=512):
        # Same logic but for .cpp files
        for filename in os.listdir(data_dir):
            if filename.endswith('.cpp'):
                # ... process
```

---

## 🎯 GIAI ĐOẠN 4: ĐÁNH GIÁ VÀ KIỂM THỬ (Tuần 4)

### A. Evaluation Script

**File: `evaluate_multilang_models.py`**

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class ModelEvaluator:
    def __init__(self, model_path, test_dir, file_extension):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        self.test_dir = test_dir
        self.file_extension = file_extension
        
    def load_test_data(self):
        files = []
        labels = []
        filenames = []
        
        for filename in os.listdir(self.test_dir):
            if filename.endswith(self.file_extension):
                filepath = os.path.join(self.test_dir, filename)
                label = int(filename.split('_')[0])
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                files.append(code)
                labels.append(label)
                filenames.append(filename)
        
        return files, labels, filenames
    
    @torch.no_grad()
    def predict(self, code):
        inputs = self.tokenizer(
            code,
            truncation=True,
            max_length=512,
            padding='max_length',
            return_tensors='pt'
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        outputs = self.model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1)
        pred = torch.argmax(probs, dim=-1).item()
        
        return pred, probs[0].cpu().numpy()
    
    def evaluate(self):
        files, labels, filenames = self.load_test_data()
        
        predictions = []
        all_probs = []
        
        print(f"Evaluating {len(files)} samples...")
        
        for code in files:
            pred, probs = self.predict(code)
            predictions.append(pred)
            all_probs.append(probs)
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(
            labels, predictions,
            target_names=['AI-Generated', 'Human-Written']
        ))
        
        # Confusion matrix
        cm = confusion_matrix(labels, predictions)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['AI', 'Human'],
                   yticklabels=['AI', 'Human'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'{self.test_dir}_confusion_matrix.png')
        print(f"Confusion matrix saved to {self.test_dir}_confusion_matrix.png")
        
        # Error analysis
        errors = []
        for i, (true, pred) in enumerate(zip(labels, predictions)):
            if true != pred:
                errors.append({
                    'filename': filenames[i],
                    'true_label': 'AI' if true == 0 else 'Human',
                    'pred_label': 'AI' if pred == 0 else 'Human',
                    'confidence': max(all_probs[i])
                })
        
        if errors:
            print(f"\nFound {len(errors)} errors:")
            for err in errors[:10]:  # Show first 10
                print(f"  {err['filename']}: True={err['true_label']}, "
                      f"Pred={err['pred_label']}, Conf={err['confidence']:.2f}")

if __name__ == "__main__":
    # Evaluate Python model
    print("=" * 50)
    print("EVALUATING PYTHON MODEL")
    print("=" * 50)
    evaluator_py = ModelEvaluator(
        model_path="./models/codebert-python-v1",
        test_dir="./DATASETS/PYTHON/testing_data",
        file_extension=".py"
    )
    evaluator_py.evaluate()
    
    # Evaluate C++ model
    print("\n" + "=" * 50)
    print("EVALUATING C++ MODEL")
    print("=" * 50)
    evaluator_cpp = ModelEvaluator(
        model_path="./models/codebert-cpp-v1",
        test_dir="./DATASETS/CPP/testing_data",
        file_extension=".cpp"
    )
    evaluator_cpp.evaluate()
```

---

## 🎯 GIAI ĐOẠN 5: TÍCH HỢP VÀO HỆ THỐNG (Tuần 5)

### A. Multi-Language Detection Service

**File: `webapp/server/multilang_detector.py`**

```python
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Optional
import mimetypes

class MultiLanguageDetector:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        self.tokenizers = {}
        
        # Load all models
        self.load_models()
    
    def load_models(self):
        """Load all language-specific models"""
        models_config = {
            'java': './models/gptsniffer-finetuned',
            'python': './models/codebert-python-v1',
            'cpp': './models/codebert-cpp-v1'
        }
        
        for lang, model_path in models_config.items():
            if os.path.exists(model_path):
                print(f"Loading {lang} model from {model_path}...")
                try:
                    self.tokenizers[lang] = AutoTokenizer.from_pretrained(model_path)
                    self.models[lang] = AutoModelForSequenceClassification.from_pretrained(model_path)
                    self.models[lang].to(self.device)
                    self.models[lang].eval()
                    print(f"✓ {lang} model loaded")
                except Exception as e:
                    print(f"✗ Failed to load {lang} model: {e}")
            else:
                print(f"⚠ Model not found: {model_path}")
    
    def detect_language(self, filename: str, code: Optional[str] = None) -> str:
        """Detect programming language from filename or code"""
        # Method 1: From extension
        ext = filename.split('.')[-1].lower()
        
        lang_map = {
            'py': 'python',
            'java': 'java',
            'cpp': 'cpp',
            'cc': 'cpp',
            'cxx': 'cpp',
            'c': 'cpp',
            'h': 'cpp',
            'hpp': 'cpp'
        }
        
        detected = lang_map.get(ext)
        
        if detected and detected in self.models:
            return detected
        
        # Method 2: Heuristics from code (if extension unclear)
        if code:
            if 'def ' in code and 'import ' in code:
                return 'python'
            elif 'public class ' in code or 'private class ' in code:
                return 'java'
            elif '#include' in code or 'std::' in code:
                return 'cpp'
        
        return 'java'  # Default fallback
    
    @torch.no_grad()
    def predict(self, code: str, language: str) -> Dict:
        """Predict if code is AI-generated"""
        if language not in self.models:
            raise ValueError(f"Language {language} not supported. Available: {list(self.models.keys())}")
        
        model = self.models[language]
        tokenizer = self.tokenizers[language]
        
        # Tokenize
        inputs = tokenizer(
            code,
            truncation=True,
            max_length=512,
            padding='max_length',
            return_tensors='pt'
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Predict
        outputs = model(**inputs)
        logits = outputs.logits.detach().cpu()
        probs = torch.softmax(logits, dim=-1).squeeze(0)
        
        ai_prob = float(probs[0])
        human_prob = float(probs[1])
        
        label = "Human" if human_prob > ai_prob else "ChatGPT"
        confidence = max(ai_prob, human_prob)
        
        return {
            "label": label,
            "confidence": confidence,
            "probabilities": {
                "ChatGPT": ai_prob,
                "Human": human_prob
            },
            "language": language,
            "model_source": f"CodeBERT-{language}",
            "device": str(self.device)
        }
    
    def predict_file(self, filename: str, code: str) -> Dict:
        """Predict with auto language detection"""
        language = self.detect_language(filename, code)
        return self.predict(code, language)

# Global instance
multilang_detector = MultiLanguageDetector()
```

### B. Update API Endpoints

**Update `webapp/server/main.py`:**

```python
from webapp.server.multilang_detector import multilang_detector

@app.post("/predict")
def predict_json(payload: PredictRequest) -> Dict[str, Any]:
    code = payload.code
    language = payload.language if hasattr(payload, 'language') else None
    
    if language:
        # User specified language
        return multilang_detector.predict(code, language)
    else:
        # Auto-detect (default to Java for backward compatibility)
        return multilang_detector.predict(code, "java")

@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    raw_bytes = await file.read()
    code = raw_bytes.decode("utf-8", errors="ignore")
    
    # Auto-detect language from filename
    return multilang_detector.predict_file(file.filename, code)

@app.get("/languages")
def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": list(multilang_detector.models.keys()),
        "default": "java"
    }
```

---

## 🎯 GIAI ĐOẠN 6: FRONTEND UPDATE (Tuần 5)

### Update UI to show language selection

**Add to `webapp/static/index.html`:**

```html
<!-- Language selector -->
<div class="form-group">
  <label for="language">Ngôn ngữ lập trình</label>
  <select id="language" class="language-select">
    <option value="auto">Tự động phát hiện</option>
    <option value="java">Java</option>
    <option value="python">Python</option>
    <option value="cpp">C/C++</option>
  </select>
</div>
```

**Update JavaScript:**

```javascript
async function predictCode() {
    const code = document.getElementById('code').value.trim();
    const language = document.getElementById('language').value;
    
    if (!code) {
        showError('Vui lòng nhập mã nguồn trước khi phân tích');
        return;
    }

    showLoading();
    try {
        const payload = {
            code: code
        };
        
        if (language !== 'auto') {
            payload.language = language;
        }
        
        const res = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        displayResult(data);
    } catch (e) {
        showError('Không thể kết nối đến máy chủ: ' + e.message);
    }
}
```

---

## 📊 TARGET METRICS

### Baseline Targets (after fine-tuning)

**Python Model:**
```
- Accuracy: ≥ 92%
- Precision: ≥ 90%
- Recall: ≥ 90%
- F1-Score: ≥ 90%
```

**C++ Model:**
```
- Accuracy: ≥ 90%
- Precision: ≥ 88%
- Recall: ≥ 88%
- F1-Score: ≥ 88%
```

---

## 📝 CHECKLIST THỰC HIỆN

### Tuần 1: Dataset Collection
- [ ] Download CodeSearchNet Python dataset
- [ ] Sample 2000 human Python code
- [ ] Collect C++ code from GitHub repos
- [ ] Create prompt templates for ChatGPT

### Tuần 2: AI Code Generation + Processing
- [ ] Generate 2000 AI Python samples
- [ ] Generate 1500 AI C++ samples
- [ ] Verify code syntax (compile check)
- [ ] Split train/test (80/20)
- [ ] Create dataset statistics report

### Tuần 3: Training Python Model
- [ ] Setup training environment (GPU)
- [ ] Run training script
- [ ] Monitor training metrics
- [ ] Evaluate on test set
- [ ] Save best checkpoint

### Tuần 4: Training C++ Model
- [ ] Prepare C++ dataset
- [ ] Run training script
- [ ] Monitor training metrics
- [ ] Evaluate on test set
- [ ] Compare with Python results

### Tuần 5: Integration
- [ ] Implement MultiLanguageDetector
- [ ] Update API endpoints
- [ ] Add language detection logic
- [ ] Update frontend UI
- [ ] End-to-end testing

### Tuần 6: Testing & Documentation
- [ ] Test all 3 languages
- [ ] Performance benchmarking
- [ ] Write user documentation
- [ ] Create demo videos
- [ ] Deploy to production

---

## 🚀 SCRIPTS READY TO RUN

Tôi sẽ tạo các scripts sẵn sàng chạy trong bước tiếp theo!
