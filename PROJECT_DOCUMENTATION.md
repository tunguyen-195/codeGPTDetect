# GPTSniffer - Hệ Thống Phát Hiện Code AI

## 📋 Tổng Quan Dự Án

**GPTSniffer** là một hệ thống machine learning để phát hiện mã nguồn được tạo bởi AI (ChatGPT, Groq, Ollama, v.v.) so với mã nguồn do con người viết. Hệ thống hỗ trợ đa ngôn ngữ lập trình và đạt độ chính xác cao.

### Thông Tin Dự Án
- **Tên:** GPTSniffer - AI Code Detection System
- **Version:** 2.0.0
- **Ngôn ngữ hỗ trợ:** Java, Python
- **Công nghệ:** CodeBERT, PyTorch, FastAPI, Transformers
- **Độ chính xác:** 100% trên test set

### Tính Năng Chính
✅ **Phát hiện mã AI-generated vs Human-written**
✅ **Hỗ trợ đa ngôn ngữ:** Java, Python (C++ ready)
✅ **Tự động nhận diện ngôn ngữ**
✅ **Chọn model linh hoạt:** Base/Java/Python
✅ **REST API đầy đủ**
✅ **Web UI hiện đại**
✅ **Độ chính xác cao:** 100% accuracy

---

## 🏗️ Kiến Trúc Hệ Thống

### Sơ Đồ Tổng Quan
```
┌─────────────────────────────────────────┐
│         Client Applications             │
│  (Web UI / API / Mobile / CLI)         │
└─────────────┬───────────────────────────┘
              │ HTTP/REST
              ▼
┌─────────────────────────────────────────┐
│       FastAPI Server (Port 8000)        │
│   webapp/server/main_multilang.py       │
│                                          │
│   Endpoints:                             │
│   - GET  /health                         │
│   - GET  /models                         │
│   - POST /predict                        │
│   - POST /predict-file                   │
│   - POST /detect-language                │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    MultiLanguageDetector                │
│    multilang_detector.py                │
│                                          │
│    - Auto language detection            │
│    - Model routing & management         │
│    - Inference orchestration            │
└─────┬───────────────┬───────────────────┘
      │               │
      ▼               ▼
┌────────────┐  ┌────────────┐  
│Java Model  │  │Python Model│  
│CodeBERT    │  │CodeBERT    │  
│Fine-tuned  │  │Fine-tuned  │  
│~85% acc    │  │100% acc    │  
└────────────┘  └────────────┘  
```

### Các Component Chính

#### 1. Models (Mô hình học máy)
- **Java Model:** `models/gptsniffer-finetuned/`
  - Base: microsoft/codebert-base
  - Fine-tuned on Java dataset
  - Accuracy: ~85%
  - Size: 450 MB

- **Python Model:** `models/python-detector-20251103_135045/`
  - Base: microsoft/codebert-base
  - Fine-tuned on Python dataset (3286 training samples)
  - Accuracy: 100% on test set (823 samples)
  - Size: 498 MB
  - Dataset cleaned (no metadata leakage)

#### 2. Backend API
- **File:** `webapp/server/main_multilang.py`
- **Framework:** FastAPI
- **Features:**
  - Multi-language detection
  - Model selection (Base/Java/Python)
  - File upload support
  - Auto language detection
  - CORS enabled
  - API documentation (Swagger)

#### 3. Frontend UI
- **File:** `webapp/static/index.html`
- **Features:**
  - Modern, responsive design
  - Language selector (Java/Python)
  - Code editor with syntax highlighting
  - Real-time prediction
  - Confidence visualization
  - File upload support

#### 4. Multi-Language Detector
- **File:** `multilang_detector.py`
- **Class:** `MultiLanguageDetector`
- **Features:**
  - Unified API for all models
  - Pattern-based language detection
  - Dynamic model loading
  - GPU/CPU support

---

## 📊 Dataset & Training

### Python Dataset
**Nguồn:**
- **Human Code:** CodeSearchNet Python dataset (2000 samples)
- **AI Code:** Generated using Ollama (qwen2.5:7b) and Groq API (2152 samples)

**Statistics:**
```
Total Samples: 4152
├── Human Code: 2000 (48.2%)
└── AI Code:    2152 (51.8%)

Training Set: 3286 samples (80%)
├── AI:    1721 (52.4%)
└── Human: 1565 (47.6%)

Test Set: 823 samples (20%)
├── AI:    431 (52.4%)
└── Human: 392 (47.6%)
```

**Dataset Cleaning:**
- Removed all metadata headers that caused data leakage
- Removed AI-generated markers, model names, categories
- Script: `clean_dataset.py`
- Files cleaned: 4304/8261 (52.1%)

### Training Configuration
```python
Model: microsoft/codebert-base
Task: Binary classification (AI vs Human)

Hyperparameters:
├── Epochs: 12 (stopped early at epoch 4)
├── Batch size: 8 (train), 16 (eval)
├── Learning rate: 5e-5
├── Weight decay: 0.01
├── Warmup steps: 500
├── Optimizer: AdamW
└── Device: CPU

Training Time: ~3.7 hours (CPU)
Best Checkpoint: Epoch 1
```

### Model Performance
```
Python Model (20251103_135045):
├── Accuracy:  100.00%
├── Precision: 100.00%
├── Recall:    100.00%
├── F1-Score:  100.00%
└── Test samples: 823

Confusion Matrix:
                 Predicted
               AI    Human
Actual  AI    431      0
        Human   0    392
```

---

## 🚀 Cài Đặt & Triển Khai

### Yêu Cầu Hệ Thống
- **Python:** 3.8+
- **RAM:** 10GB+ (để load models)
- **Storage:** 2GB+ (cho models và datasets)
- **OS:** Windows 10/11, Linux, macOS
- **GPU:** Optional (CUDA 11.0+ nếu có)

### Cài Đặt Dependencies
```bash
# Clone repository
git clone https://github.com/your-repo/GPTSniffer.git
cd GPTSniffer

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install torch transformers fastapi uvicorn scikit-learn pandas numpy matplotlib seaborn tqdm requests
```

### Cấu Trúc Thư Mục
```
GPTSniffer/
├── models/                          # Model files
│   ├── gptsniffer-finetuned/        # Java model
│   └── python-detector-20251103_135045/  # Python model
│
├── DATASETS/                        # Training & test data
│   └── PYTHON/
│       ├── raw/
│       │   ├── ai/                  # AI-generated code
│       │   └── human/               # Human-written code
│       ├── training_data/           # Training set
│       └── testing_data/            # Test set
│
├── webapp/                          # Web application
│   ├── server/
│   │   └── main_multilang.py       # FastAPI server
│   └── static/
│       └── index.html               # Frontend UI
│
├── multilang_detector.py            # Core detector
├── train_python_model.py            # Training script
├── test_python_model.py             # Testing script
├── clean_dataset.py                 # Dataset cleaning
├── evaluate_model.py                # Comprehensive evaluation
├── test_api_quick.py                # API testing
│
└── Documentation/
    ├── README.md
    ├── QUICKSTART.md
    ├── TRAINING_GUIDE.md
    ├── DEPLOYMENT_GUIDE_MULTILANG.md
    └── PROJECT_DOCUMENTATION.md     # This file
```

---

## 🎯 Sử Dụng

### 1. Khởi Động Server

#### Cách 1: Chạy Trực Tiếp
```bash
cd GPTSniffer
python webapp/server/main_multilang.py
```

#### Cách 2: Sử dụng Script
```bash
# Windows:
.\start_multilang_server.bat

# Linux/Mac:
./start_multilang_server.sh
```

**Server sẽ chạy tại:**
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Web UI: http://localhost:8000

### 2. Sử Dụng Web UI

1. Mở browser: http://localhost:8000
2. Chọn ngôn ngữ: Java hoặc Python
3. Nhập hoặc paste code vào editor
4. Click "Phân tích mã nguồn"
5. Xem kết quả:
   - Label: AI-Generated hoặc Human-Written
   - Confidence: Độ tin cậy (%)
   - Probabilities: Xác suất chi tiết

**Hoặc upload file:**
1. Click "Tải lên file"
2. Chọn file .java hoặc .py
3. Xem kết quả tự động

### 3. Sử Dụng API

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Get Available Models
```bash
curl http://localhost:8000/models
```

#### Predict (Auto Language Detection)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
  }'
```

#### Predict (Explicit Language)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public class Test { }",
    "language": "java"
  }'
```

#### Predict (Specific Model)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def test(): pass",
    "model": "python"
  }'
```

#### Upload File
```bash
curl -X POST http://localhost:8000/predict-file \
  -F "file=@example.py" \
  -F "language=python"
```

### 4. Sử Dụng Python SDK

```python
from multilang_detector import get_detector

# Initialize detector
detector = get_detector()

# Predict with auto-detection
python_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    return quicksort([x for x in arr if x < pivot]) + [pivot] + quicksort([x for x in arr if x > pivot])
"""

result = detector.predict(python_code)
print(f"Language: {result['language']}")
print(f"Prediction: {result['label']}")
print(f"Confidence: {result['confidence']:.2%}")

# Predict with specific model
result = detector.predict(python_code, model='python')
print(f"Model: {result['model_used']}")
print(f"Prediction: {result['label']}")
```

---

## 🔬 Testing & Evaluation

### Test Model
```bash
# Test Python model
python test_python_model.py

# Quick API test
python test_api_quick.py

# Comprehensive evaluation
python evaluate_model.py
```

### Expected Output
```
Testing Python Model:
✓ Human code: 100.0% confidence
✓ AI code: 100.0% confidence
✓ Real files: 6/6 correct (100%)

API Testing:
✓ Health check: OK
✓ Models endpoint: OK
✓ Auto-detection: Working
✓ Explicit language: Working
✓ Model selection: Working
```

---

## 📈 Performance Metrics

### Model Performance
| Metric | Python Model | Java Model |
|--------|-------------|------------|
| Accuracy | 100.00% | ~85% |
| Precision | 100.00% | ~85% |
| Recall | 100.00% | ~85% |
| F1-Score | 100.00% | ~85% |
| Test Samples | 823 | N/A |

### API Performance
| Metric | Value |
|--------|-------|
| Response Time | ~100-200ms |
| Throughput | ~5-10 req/s |
| Model Load Time | ~5-10s |
| Memory Usage | ~10GB |

### Resource Usage
| Component | CPU | RAM | Storage |
|-----------|-----|-----|---------|
| Java Model | Low | ~5GB | 450MB |
| Python Model | Low | ~5GB | 498MB |
| API Server | Low | ~100MB | Minimal |
| **Total** | Low | **~10GB** | **~1GB** |

---

## 🔧 Configuration

### Model Paths
Edit `multilang_detector.py`:
```python
self.model_paths = {
    'base': 'microsoft/codebert-base',
    'java': 'models/gptsniffer-finetuned',
    'python': 'models/python-detector-20251103_135045',
    # 'cpp': 'models/cpp-detector-xxx',  # Future
}
```

### Server Configuration
Edit `webapp/server/main_multilang.py`:
```python
# Change port
uvicorn.run(app, host="0.0.0.0", port=8000)

# Enable HTTPS (production)
uvicorn.run(
    app, 
    host="0.0.0.0", 
    port=443,
    ssl_keyfile="/path/to/key.pem",
    ssl_certfile="/path/to/cert.pem"
)
```

---

## 🐛 Troubleshooting

### Model Not Loading
**Lỗi:** `Model not found at path`
**Giải pháp:**
1. Kiểm tra đường dẫn model trong `multilang_detector.py`
2. Đảm bảo model đã được train và lưu đúng
3. Kiểm tra quyền đọc file

### Out of Memory
**Lỗi:** `CUDA out of memory` hoặc `RAM insufficient`
**Giải pháp:**
1. Giảm batch size trong training
2. Sử dụng CPU thay vì GPU
3. Tăng RAM (cần ít nhất 10GB)
4. Load từng model riêng lẻ

### Server Won't Start
**Lỗi:** `Port 8000 already in use`
**Giải pháp:**
```bash
# Windows: Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Or change port in main_multilang.py
```

### API Returns Errors
**Lỗi:** `500 Internal Server Error`
**Giải pháp:**
1. Kiểm tra logs trong terminal
2. Verify model files tồn tại
3. Kiểm tra PYTHONPATH
4. Restart server

---

## 🚀 Deployment

### Local Deployment
```bash
# Already covered above
python webapp/server/main_multilang.py
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "webapp/server/main_multilang.py"]
```

```bash
# Build & Run
docker build -t gptsniffer:latest .
docker run -p 8000:8000 gptsniffer:latest
```

### Production Deployment (Linux)
```bash
# 1. Install systemd service
sudo nano /etc/systemd/system/gptsniffer.service

# Content:
[Unit]
Description=GPTSniffer API Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/GPTSniffer
Environment="PYTHONPATH=/path/to/GPTSniffer"
ExecStart=/path/to/.venv/bin/python webapp/server/main_multilang.py
Restart=always

[Install]
WantedBy=multi-user.target

# 2. Enable & start
sudo systemctl daemon-reload
sudo systemctl enable gptsniffer
sudo systemctl start gptsniffer
sudo systemctl status gptsniffer

# 3. Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/gptsniffer

# Content:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 4. Enable site
sudo ln -s /etc/nginx/sites-available/gptsniffer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📚 API Documentation

### Endpoints

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "GPTSniffer Multi-Language Detector",
  "version": "2.0.0",
  "supported_languages": ["java", "python"],
  "available_models": ["java", "python"]
}
```

#### GET /models
Get available models.

**Response:**
```json
{
  "available_models": ["java", "python"],
  "model_descriptions": {
    "base": "CodeBERT Base (Chưa fine-tune)",
    "java": "Java Detector (Fine-tuned)",
    "python": "Python Detector (100% accuracy)"
  },
  "count": 2
}
```

#### POST /predict
Predict code origin.

**Request:**
```json
{
  "code": "def test(): pass",
  "language": "python",  // optional
  "model": "python"      // optional
}
```

**Response:**
```json
{
  "label": "AI-Generated",
  "confidence": 0.9987,
  "probabilities": {
    "AI-Generated": 0.9987,
    "Human-Written": 0.0013
  },
  "language": "PYTHON",
  "auto_detected": true,
  "model_used": "python",
  "model_description": "Python Detector (100% accuracy)",
  "device": "cpu"
}
```

#### POST /predict-file
Upload and predict file.

**Request (multipart/form-data):**
- `file`: File to upload (.java or .py)
- `language`: Optional language hint

**Response:** Same as /predict

#### POST /detect-language
Detect programming language.

**Request:**
```json
{
  "code": "def test(): pass"
}
```

**Response:**
```json
{
  "language": "python",
  "confidence": "high"
}
```

---

## 🎓 Training New Models

### Collect Dataset
```bash
# For Python (already done)
# Human: CodeSearchNet
# AI: Groq API + Ollama

# For C++ (future)
python scripts/download_cpp_dataset.py
python generate_ollama.py --language cpp --num 2000
```

### Prepare Dataset
```bash
# Clean metadata
python clean_dataset.py

# Split train/test
python scripts/prepare_dataset.py --language python --train-ratio 0.8
```

### Train Model
```bash
# Train Python model
python train_python_model.py

# Train C++ model (future)
python train_cpp_model.py
```

### Evaluate Model
```bash
# Test on samples
python test_python_model.py

# Comprehensive evaluation
python evaluate_model.py
```

### Update Paths
```python
# Edit multilang_detector.py
self.model_paths = {
    ...
    'python': 'models/python-detector-{NEW_TIMESTAMP}',
}
```

---

## 🔐 Security Considerations

### Code Input Validation
- Sanitize user input
- Limit code length (max 10,000 chars)
- Check for malicious code patterns
- Rate limiting API requests

### Model Security
- Models are read-only
- No code execution on server
- Sandbox predictions
- Log all requests

### Deployment Security
```bash
# Use HTTPS in production
# Enable firewall
sudo ufw allow 443/tcp
sudo ufw enable

# Set proper file permissions
chmod 600 models/*
chmod 644 webapp/static/*
chmod 755 webapp/server/*.py
```

---

## 📖 References

### Paper
- **Title:** GPTSniffer: A CodeBERT-based classifier to detect source code written by ChatGPT
- **Authors:** Phuong T. Nguyen, et al.
- **Journal:** Journal of Systems and Software (JSS)
- **Link:** https://www.sciencedirect.com/science/article/pii/S0164121224001043

### Technologies
- **CodeBERT:** https://github.com/microsoft/CodeBERT
- **Transformers:** https://huggingface.co/docs/transformers
- **FastAPI:** https://fastapi.tiangolo.com/
- **PyTorch:** https://pytorch.org/

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Contact & Support

- **Email:** phuong.nguyen@univaq.it
- **GitHub:** https://github.com/your-repo/GPTSniffer
- **Issues:** https://github.com/your-repo/GPTSniffer/issues

---

## 🎉 Acknowledgments

- Università degli Studi dell'Aquila, Italy
- CodeSearchNet dataset
- Microsoft CodeBERT team
- Open-source community

---

**Last Updated:** November 5, 2025
**Version:** 2.0.0
**Status:** Production Ready ✅
