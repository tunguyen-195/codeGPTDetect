# 🚀 HƯỚNG DẪN SỬ DỤNG NHANH - GPTSniffer

## ⚡ Khởi Động Nhanh (2 Phút)

### Bước 1: Khởi động Server

```bash
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
.\start.bat
```

> **Lưu ý**: Hoặc sử dụng command: `python -m app.main`

### Bước 2: Mở Web UI

Mở trình duyệt và truy cập: **<http://localhost:8000>**

### Bước 3: Sử dụng

1. Chọn ngôn ngữ: **Java** hoặc **Python**
2. Nhập code vào ô editor
3. Click **"Phân tích mã nguồn"**
4. Xem kết quả!

---

## 📖 Hướng Dẫn Chi Tiết

### 1️⃣ Sử Dụng Web Interface

#### Phân tích code Python

1. Mở <http://localhost:8000>
2. Chọn **"Python Model"** từ dropdown
3. Paste code Python vào editor, ví dụ:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

4. Click **"Phân tích mã nguồn"**

#### Kết quả hiển thị

- **Label:** AI-Generated hoặc Human-Written
- **Confidence:** Độ tin cậy (0-100%)
- **Probabilities:** Xác suất chi tiết cho từng loại
- **Model:** Model đã sử dụng để phân tích

#### Upload file

1. Click **"Tải lên file"**
2. Chọn file `.py` hoặc `.java`
3. Kết quả hiển thị tự động

---

### 2️⃣ Sử Dụng API (Lập trình viên)

#### Test với curl

**Health Check:**

```bash
curl http://localhost:8000/health
```

**Phân tích Python code:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"def test(): pass\", \"model\": \"python\"}"
```

**Phân tích Java code:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"public class Test {}\", \"model\": \"java\"}"
```

#### Sử dụng Python

```python
import requests

# API endpoint
url = "http://localhost:8000/predict"

# Code muốn phân tích
code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    return quicksort([x for x in arr if x < pivot]) + [pivot] + quicksort([x for x in arr if x > pivot])
"""

# Gửi request
response = requests.post(url, json={
    "code": code,
    "model": "python"  # hoặc "java"
})

# Xem kết quả
result = response.json()
print(f"Prediction: {result['label']}")
print(f"Confidence: {result['confidence']*100:.2f}%")
```

#### Sử dụng JavaScript

```javascript
const code = `
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
`;

fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: code,
    model: 'python'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Prediction:', data.label);
  console.log('Confidence:', data.confidence);
});
```

---

### 3️⃣ API Endpoints

#### GET /health

Kiểm tra trạng thái server

**Response:**

```json
{
  "status": "ok",
  "service": "GPTSniffer Multi-Language Detector",
  "version": "2.0.0",
  "supported_languages": ["java", "python"]
}
```

#### GET /models

Lấy danh sách models có sẵn

**Response:**

```json
{
  "available_models": ["java", "python"],
  "model_descriptions": {
    "java": "Java Detector (Fine-tuned)",
    "python": "Python Detector (100% accuracy)"
  }
}
```

#### POST /predict

Phân tích code

**Request Body:**

```json
{
  "code": "def test(): pass",
  "model": "python",      // tùy chọn: "base", "java", "python"
  "language": "python"    // tùy chọn: "java", "python"
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
  "model_used": "python",
  "model_description": "Python Detector (100% accuracy)"
}
```

#### POST /predict-file

Upload file để phân tích

**Request (multipart/form-data):**

- `file`: File cần phân tích (.py hoặc .java)
- `language`: Ngôn ngữ (tùy chọn)

**Response:** Giống /predict

#### POST /detect-language

Tự động nhận diện ngôn ngữ

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

## 🎯 Các Trường Hợp Sử Dụng

### Use Case 1: Giáo viên kiểm tra bài tập

```
Tình huống: Giáo viên nghi ngờ sinh viên dùng AI làm bài
Cách làm:
1. Mở web UI
2. Paste code của sinh viên
3. Chọn ngôn ngữ (Java/Python)
4. Xem kết quả
   - Nếu AI-Generated > 90%: Có khả năng dùng AI
   - Nếu Human-Written > 90%: Có khả năng tự làm
```

### Use Case 2: Code review trong dự án

```
Tình huống: Team lead muốn đảm bảo code là do developer tự viết
Cách làm:
1. Tích hợp API vào CI/CD pipeline
2. Tự động scan các file code mới commit
3. Flag nếu phát hiện AI-generated code
4. Yêu cầu developer giải thích
```

### Use Case 3: Nghiên cứu học thuật

```
Tình huống: Nghiên cứu sự khác biệt giữa AI code vs Human code
Cách làm:
1. Sử dụng Python SDK
2. Phân tích hàng loạt file code
3. Thu thập statistics
4. Phân tích patterns
```

---

## 📊 Hiểu Kết Quả

### Confidence Score

- **90-100%**: Rất chắc chắn
- **70-89%**: Khá chắc chắn
- **50-69%**: Không chắc chắn
- **<50%**: Kết quả không đáng tin cậy

### Label Meanings

- **AI-Generated**: Code có khả năng cao do AI tạo ra
  - Đặc điểm: Comment chi tiết, docstrings, type hints, format chuẩn
- **Human-Written**: Code có khả năng do con người viết
  - Đặc điểm: Style đa dạng, ít comment, có thể có lỗi nhỏ

### Probabilities

```json
{
  "AI-Generated": 0.9987,    // 99.87% là AI
  "Human-Written": 0.0013    // 0.13% là Human
}
```

Tổng luôn = 1.0 (100%)

---

## ⚙️ Tùy Chọn Nâng Cao

### Chọn Model Cụ Thể

```bash
# Dùng Python model (chính xác nhất cho Python code)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "...", "model": "python"}'

# Dùng Java model (chính xác nhất cho Java code)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "...", "model": "java"}'

# Dùng Base model (universal, accuracy thấp hơn)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "...", "model": "base"}'
```

### Tự Động Nhận Diện Ngôn Ngữ

```bash
# Không chỉ định model, hệ thống tự detect
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "def test(): pass"}'

# System sẽ:
# 1. Detect language = Python
# 2. Auto chọn Python model
# 3. Return prediction
```

---

## 🐛 Xử Lý Lỗi

### Lỗi 1: Server không khởi động

```
Lỗi: "Port 8000 already in use"
Giải pháp:
- Windows: taskkill /F /IM python.exe
- Linux: killall python
- Hoặc đổi port trong main_multilang.py
```

### Lỗi 2: Model không load

```
Lỗi: "Model not found"
Giải pháp:
1. Kiểm tra đường dẫn trong multilang_detector.py
2. Đảm bảo folder models/ tồn tại
3. Download lại models nếu cần
```

### Lỗi 3: API trả về 500

```
Lỗi: "Internal Server Error"
Giải pháp:
1. Xem logs trong terminal
2. Kiểm tra code input có hợp lệ
3. Restart server
```

### Lỗi 4: Out of Memory

```
Lỗi: "Cannot allocate memory"
Giải pháp:
1. Cần ít nhất 10GB RAM
2. Đóng các ứng dụng khác
3. Hoặc dùng cloud server
```

---

## 💡 Tips & Best Practices

### Tip 1: Chọn Model Đúng

- **Python code** → Dùng Python model (100% accuracy)
- **Java code** → Dùng Java model (~85% accuracy)
- **Code lạ** → Dùng Base model (universal)

### Tip 2: Code Cần Đủ Dài

- **Tốt nhất:** 50-500 dòng code
- **OK:** 20-50 dòng
- **Không tốt:** <20 dòng (accuracy giảm)

### Tip 3: Giữ Code Nguyên Gốc

- Không format lại code trước khi test
- Giữ nguyên comments, docstrings
- Giữ nguyên style gốc

### Tip 4: Interpret Results

- Confidence >90%: Tin cậy
- Confidence 70-90%: Cần kiểm tra thêm
- Confidence <70%: Kết quả không chắc chắn

---

## 📞 Hỗ Trợ

### Liên Hệ

- **Email:** <support@gptsniffer.com>
- **GitHub Issues:** <https://github.com/your-repo/GPTSniffer/issues>

### Tài Liệu

- **Full Documentation:** PROJECT_DOCUMENTATION.md
- **Training Guide:** TRAINING_GUIDE.md
- **Deployment Guide:** DEPLOYMENT_GUIDE_MULTILANG.md
- **API Docs:** <http://localhost:8000/docs> (khi server chạy)

---

## ✅ Checklist Sử Dụng

- [ ] Server đã khởi động (<http://localhost:8000>)
- [ ] Health check OK (curl <http://localhost:8000/health>)
- [ ] Web UI hoạt động
- [ ] Đã test với code mẫu
- [ ] Hiểu cách đọc kết quả
- [ ] Biết cách chọn model phù hợp

---

**Chúc bạn sử dụng GPTSniffer hiệu quả!** 🎉

*Last Updated: November 5, 2025*
