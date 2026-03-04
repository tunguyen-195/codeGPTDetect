# T07GPTcodeDetect

> **Hệ thống phát hiện code được sinh bởi các mô hình ngôn ngữ lớn**
> AI-generated code detection using fine-tuned CodeBERT models (Python & Java)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Cài Đặt Nhanh (Windows)

### Bước 1 — Clone repo

```bash
git clone https://github.com/tunguyen-195/codeGPTDetect.git
cd codeGPTDetect
```

### Bước 2 — Copy models (thủ công)

Models không được push lên git vì quá lớn (~1GB). Cần copy từ máy gốc:

```
Cấu trúc cần có sau khi copy:

codeGPTDetect/
└── models/
    ├── java-detector-finetuned/
    │   ├── config.json
    │   ├── model.safetensors      ← ~498 MB
    │   ├── tokenizer.json
    │   ├── tokenizer_config.json
    │   ├── vocab.json
    │   └── merges.txt
    │
    └── python-detector-finetuned/
        ├── config.json
        ├── model.safetensors      ← ~498 MB
        ├── tokenizer.json
        ├── tokenizer_config.json
        ├── vocab.json
        └── merges.txt
```

> Xem mục **"Cách Copy Models"** bên dưới để biết cách lấy files từ máy gốc.

### Bước 3 — Chạy SETUP.bat

Double-click hoặc chạy trong terminal:

```
SETUP.bat
```

File này tự động:
- Kiểm tra Python
- Tạo virtual environment (`.venv`)
- Cài tất cả thư viện từ `requirements.txt`
- Tạo file `.env`
- Khởi tạo database với tài khoản admin

### Bước 4 — Chạy server

```
start.bat
```

Mở trình duyệt: **http://localhost:8000**

| Tài khoản | Giá trị |
|-----------|---------|
| Email | `admin@t07.com` |
| Mật khẩu | `a` |

---

## Cách Copy Models Từ Máy Gốc

### Cách 1: USB / ổ cứng ngoài

Trên **máy gốc**, copy 2 thư mục:
```
E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\models\java-detector-finetuned\
E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer\models\python-detector-finetuned\
```

Dán vào **máy mới** tại:
```
<thư mục clone>\models\java-detector-finetuned\
<thư mục clone>\models\python-detector-finetuned\
```

### Cách 2: Mạng LAN (nhanh hơn USB)

Trên **máy gốc** — chia sẻ thư mục models qua mạng:
1. Chuột phải thư mục `models` → Share → Everyone (Read)
2. Ghi lại địa chỉ IP máy gốc (ví dụ: `192.168.1.10`)

Trên **máy mới** — copy qua mạng:
```
\\192.168.1.10\models\java-detector-finetuned   →   models\java-detector-finetuned
\\192.168.1.10\models\python-detector-finetuned →   models\python-detector-finetuned
```

### Cách 3: Google Drive / OneDrive

Upload 2 thư mục model lên Drive, download về máy mới rồi giải nén vào `models/`.

---

## Yêu Cầu Hệ Thống

| Thành phần | Yêu cầu |
|-----------|---------|
| OS | Windows 10/11 (hoặc Linux/macOS) |
| Python | 3.10 hoặc 3.11 (khuyến nghị) |
| RAM | Tối thiểu 8GB (16GB khuyến nghị) |
| Disk | ~2GB trống (cho models + thư viện) |
| GPU | Không bắt buộc (CPU cũng chạy được) |

> **Lưu ý Python**: Khi cài, nhớ tick **"Add Python to PATH"**

---

## Cấu Trúc Dự Án

```
codeGPTDetect/
├── SETUP.bat                  ← Chạy lần đầu tiên
├── start.bat                  ← Chạy hàng ngày
├── app/                       ← Backend FastAPI
│   ├── main.py
│   ├── config.py
│   ├── api/                   ← API routes
│   ├── services/              ← Business logic + ML
│   └── schemas/               ← Request/Response models
├── frontend/                  ← Giao diện người dùng
│   ├── index.html
│   └── js/
├── models/                    ← ML models (copy thủ công)
│   ├── java-detector-finetuned/
│   └── python-detector-finetuned/
├── scripts/
│   ├── init_db.py             ← Khởi tạo database
│   └── reset_db.py            ← Reset database
├── requirements.txt
└── .env                       ← Cấu hình (tự tạo từ SETUP.bat)
```

---

## API

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | Trang chủ |
| `/health` | GET | Kiểm tra server |
| `/docs` | GET | Swagger UI |
| `/api/auth/login` | POST | Đăng nhập |
| `/api/auth/register` | POST | Đăng ký |
| `/api/analysis/predict` | POST | Phân tích code |
| `/api/analysis/models` | GET | Danh sách models |

### Ví dụ gọi API

```bash
curl -X POST http://localhost:8000/api/analysis/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"world\")", "language": "python"}'
```

---

## Models

| Model | Ngôn ngữ | Accuracy | AUC |
|-------|----------|----------|-----|
| `python-detector-finetuned` | Python | 84% | 0.925 |
| `java-detector-finetuned` | Java | ~85% | — |

Label mapping: `0 = AI-Generated`, `1 = Human-Written`

---

## Troubleshooting

**Lỗi "No module named..."**
```bat
.venv\Scripts\pip install -r requirements.txt
```

**Lỗi model không load**
- Kiểm tra `models/python-detector-finetuned/model.safetensors` có tồn tại không
- File phải ~498MB, nếu nhỏ hơn là copy bị lỗi

**Port 8000 bị chiếm**
- Mở `.env`, đổi `PORT=8001`
- Hoặc tắt ứng dụng đang dùng port 8000

**Server chạy chậm lần đầu**
- Bình thường — đang load model vào RAM (~30 giây)
- Lần sau sẽ nhanh hơn vì OS cache

---

## License

MIT License — free to use for research and education.
