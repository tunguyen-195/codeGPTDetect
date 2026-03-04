# GPTSniffer Multi-Language - Quick Start Guide

## 🚀 Khởi động nhanh

### Cách 1: Sử dụng Batch File (Đơn giản nhất)

```batch
# Double-click file này:
start_multilang_server.bat
```

### Cách 2: Command Line

```bash
# Kích hoạt virtual environment
.\.venv\Scripts\activate

# Chạy server
python webapp/server/main_multilang.py
```

### Cách 3: Python trực tiếp

```bash
.\.venv\Scripts\python.exe webapp/server/main_multilang.py
```

---

## 🌐 Truy cập hệ thống

### Web UI
- **URL:** http://localhost:8000/
- **Tính năng:**
  - Chọn ngôn ngữ (Tự động / Java / Python)
  - Nhập code trực tiếp
  - Upload file code
  - Xem kết quả chi tiết

### API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 💻 Sử dụng Web UI

### 1. Chọn ngôn ngữ

Có 3 lựa chọn:
- **Tự động** (mặc định) - Hệ thống tự phát hiện ngôn ngữ
- **Java** - Chỉ định rõ là Java code
- **Python** - Chỉ định rõ là Python code

### 2. Nhập code

**Cách 1: Dán code trực tiếp**
1. Nhập/dán code vào ô textarea
2. Click "Phân tích mã nguồn"

**Cách 2: Upload file**
1. Click "Chọn tệp"
2. Chọn file .py hoặc .java
3. Click "Tải lên & Phân tích"

### 3. Xem kết quả

Kết quả hiển thị:
- **Label:** 🤖 Code AI hoặc 👤 Code Người viết
- **Độ tin cậy:** Phần trăm confidence
- **Ngôn ngữ:** Java/Python (đã phát hiện)
- **Xác suất:** AI-Generated vs Human-Written
- **Progress bars:** Visualization của probabilities

---

## 🔧 API Usage

### Endpoint: /predict

**Auto-detect language:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(\"Hi\")",
    "language": null
  }'
```

**Explicit language:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "code": "public class Test {}",
    "language": "java"
  }'
```

**Response:**
```json
{
  "label": "Human-Written",
  "confidence": 0.9999,
  "probabilities": {
    "AI-Generated": 0.0001,
    "Human-Written": 0.9999
  },
  "language": "PYTHON",
  "auto_detected": true,
  "model": "python-detector",
  "device": "cpu"
}
```

---

## 📝 Ví dụ code để test

### Python Code (Human-written)
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

### Java Code (AI-generated)
```java
/**
 * Binary Search Tree Implementation
 */
public class BinarySearchTree {
    private Node root;
    
    class Node {
        int value;
        Node left, right;
        
        Node(int value) {
            this.value = value;
            left = right = null;
        }
    }
    
    public void insert(int value) {
        root = insertRec(root, value);
    }
    
    private Node insertRec(Node root, int value) {
        if (root == null) {
            root = new Node(value);
            return root;
        }
        
        if (value < root.value)
            root.left = insertRec(root.left, value);
        else if (value > root.value)
            root.right = insertRec(root.right, value);
            
        return root;
    }
}
```

---

## 🎯 Features

### 1. Auto Language Detection
Hệ thống tự động phát hiện ngôn ngữ dựa trên:
- Python: `def`, `class:`, `import`, `if __name__`
- Java: `public class`, `System.out`, `package`

### 2. Multi-Model Support
- Java Model: Original GPTSniffer fine-tuned
- Python Model: 100% accuracy, trained on 4152 samples

### 3. File Upload
Hỗ trợ upload file:
- `.py` - Python files
- `.java` - Java files
- `.cpp`, `.c` - C++ files (reserved)

### 4. Detailed Results
- Prediction label với emoji
- Confidence score with color coding
- Language detection status
- Model information
- Probability visualization

---

## ⚙️ Configuration

### Change Server Port

Edit `webapp/server/main_multilang.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

### Change API URL in UI

Edit `webapp/static/index.html`:
```javascript
const API_URL = 'http://localhost:8000';  // Change URL here
```

---

## 🐛 Troubleshooting

### Server không start

**Problem:** Port 8000 đã được sử dụng

**Solution:**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or change port in code
```

### UI không kết nối được API

**Problem:** CORS error hoặc connection refused

**Solution:**
1. Check server đang chạy: http://localhost:8000/health
2. Check CORS settings trong `main_multilang.py`
3. Clear browser cache

### Model prediction sai

**Problem:** Prediction không chính xác

**Solution:**
1. Check language selection (auto vs explicit)
2. Ensure code snippet đủ dài (>50 characters)
3. Try với explicit language selection

---

## 📊 Performance Tips

### 1. GPU Acceleration (Optional)
Nếu có GPU:
```python
# Models sẽ tự động sử dụng CUDA nếu có
# Expected speedup: 10x faster
```

### 2. Code Length
- Minimum: 50 characters
- Recommended: 200-500 characters
- Maximum: 512 tokens (auto-truncated)

### 3. Batch Processing
Để analyze nhiều files:
```bash
# Use API với loop
for file in *.py; do
    curl -X POST http://localhost:8000/predict-file \
      -F "file=@$file"
done
```

---

## 📱 Mobile Support

UI responsive, hỗ trợ mobile:
- Tối ưu cho màn hình nhỏ
- Touch-friendly buttons
- Responsive layout

---

## 🔒 Security Notes

### Local Development
- Server chạy trên localhost (127.0.0.1)
- Chỉ accessible từ máy local
- Safe cho development

### Production Deployment
Khi deploy production, cần:
1. Change host từ `0.0.0.0` sang specific IP
2. Add authentication
3. Configure CORS properly
4. Use HTTPS
5. Add rate limiting

---

## 📞 Support

### Docs
- API Docs: http://localhost:8000/docs
- Deployment Guide: `DEPLOYMENT_GUIDE_MULTILANG.md`
- Full Report: `MODULE5_FINAL_REPORT.md`

### Common Issues
1. Server won't start → Check port availability
2. Model not loading → Check model paths in `multilang_detector.py`
3. Prediction errors → Check code length and language selection

---

## 🎉 Quick Test

1. Start server: `start_multilang_server.bat`
2. Open browser: http://localhost:8000/
3. Select "Tự động" language
4. Paste this Python code:
```python
def hello():
    print("Hello World")
```
5. Click "Phân tích mã nguồn"
6. See result: Should detect as Python with high confidence

---

## 📝 Notes

- **First load:** Models load khi start (5-10 giây)
- **Response time:** ~100-200ms per request
- **Supported languages:** Java, Python
- **C++ support:** Ready (chỉ cần add model)

---

**Happy Detecting! 🔍**

*GPTSniffer Multi-Language v2.0.0*
