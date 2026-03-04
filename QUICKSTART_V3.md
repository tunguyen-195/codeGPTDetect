# 🚀 GPTSniffer v3.0 - QUICKSTART GUIDE

**Bắt đầu trong 5 phút!**

---

## ⚡ TL;DR (Super Quick Start)

### Windows:
```cmd
# Double-click file này hoặc chạy:
start.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

**Xong!** Mở trình duyệt: http://localhost:8000

---

## 📋 Yêu Cầu Hệ Thống

- **Python:** 3.10 trở lên
- **RAM:** 8GB minimum (16GB recommended)
- **Disk:** 5GB free space
- **OS:** Windows, Linux, macOS

Kiểm tra Python:
```bash
python --version
# Hoặc
python3 --version
```

Nếu chưa có Python, tải tại: https://www.python.org/downloads/

---

## 🎯 Cài Đặt Chi Tiết

### Bước 1: Clone Repository

```bash
git clone <your-repo-url>
cd GPTSniffer
```

### Bước 2: Tạo Virtual Environment

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý:** Nếu gặp lỗi, thử:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cấu Hình (Optional)

```bash
# Copy environment template
cp .env.example .env

# Edit .env nếu cần (optional cho development)
# SECRET_KEY, DATABASE_URL, etc.
```

### Bước 5: Initialize Database

```bash
python scripts/init_db.py
```

Khi được hỏi, nhập thông tin admin hoặc để mặc định:
- **Email:** admin@gptsniffer.com
- **Username:** admin
- **Password:** Admin@123
- **Full Name:** System Administrator

⚠️ **QUAN TRỌNG:** Đổi password sau khi đăng nhập lần đầu!

### Bước 6: Khởi Động Server

```bash
python -m app.main
```

Hoặc dùng uvicorn:
```bash
uvicorn app.main:app --reload
```

### Bước 7: Mở Trình Duyệt

Truy cập: **http://localhost:8000**

---

## 🎮 Sử Dụng Ngay

### 1. Đăng Nhập

- Mở http://localhost:8000
- Click **"Đăng Nhập"**
- Nhập credentials admin (từ Bước 5)
- Click **"Đăng Nhập"**

### 2. Phân Tích Code

- Vào **Dashboard**
- Chọn ngôn ngữ: **Python** / **Java** / **C++** / **Auto**
- Chọn model: **Auto** (recommended)
- Paste code vào editor
- Click **"Phân Tích Code"** 🔍
- Xem kết quả! 🎉

### 3. Xem Lịch Sử

- Scroll xuống **"Lịch Sử Gần Đây"**
- Xem tất cả phân tích đã lưu
- Click 🗑️ để xóa

### 4. Xem Thống Kê

- Xem **Stats Cards** ở đầu Dashboard:
  - Tổng Phân Tích
  - AI Code Detected
  - Human Code Detected
  - Độ Chính Xác TB

---

## 🔑 Tài Khoản Mặc Định

### Admin Account
```
Email:    admin@gptsniffer.com
Username: admin
Password: Admin@123
Role:     admin
```

### Test User (Tạo mới)
- Click **"Đăng Ký"**
- Điền form
- Password: min 8 chars, có uppercase, lowercase, digit
- Ví dụ: `Test123!`

---

## 📱 Các Trang Chính

| Trang | URL | Mô Tả |
|-------|-----|-------|
| **Home** | http://localhost:8000 | Landing page |
| **Dashboard** | http://localhost:8000 | Main app (sau khi login) |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Health** | http://localhost:8000/health | Health check |

---

## 🧪 Test API

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

Lưu `access_token` từ response!

### 4. Analyze Code
```bash
curl -X POST http://localhost:8000/api/analysis \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "code": "def hello():\n    print(\"Hello World\")",
    "language": "python",
    "model": "python",
    "save_to_history": true
  }'
```

---

## 🐛 Troubleshooting

### Lỗi: Module not found

```bash
# Đảm bảo virtual environment đã activate
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: Port 8000 đã được sử dụng

```bash
# Chạy trên port khác
uvicorn app.main:app --port 8001

# Hoặc kill process đang dùng port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Lỗi: Database locked

```bash
# Stop server
# Delete database
rm gptsniffer.db

# Recreate
python scripts/init_db.py

# Restart server
```

### Lỗi: Model not found

```bash
# Đảm bảo models folder tồn tại:
# models/python-detector-20251103_135045/
# models/gptsniffer-finetuned/

# Nếu không có, models sẽ fallback về random prediction
# (Chỉ để demo, không phải production)
```

### Lỗi: Permission denied (Linux/Mac)

```bash
chmod +x start.sh
chmod +x scripts/init_db.py
```

---

## 📚 Tài Liệu Đầy Đủ

- **README:** [README_V3.md](README_V3.md)
- **Technical Plan:** [WEBAPP_UPGRADE_PLAN.md](WEBAPP_UPGRADE_PLAN.md)
- **Progress:** [MODULE5_PROGRESS.md](MODULE5_PROGRESS.md)
- **Final Summary:** [FINAL_SUMMARY_V3.md](FINAL_SUMMARY_V3.md)

---

## 💡 Tips

### 1. Code Examples

**Python (AI-like):**
```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
```

**Java (Human-like):**
```java
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

### 2. Keyboard Shortcuts

- `Ctrl + Enter`: Submit form (login/register)
- `Esc`: Close modal
- `Tab`: Navigate forms

### 3. Best Practices

- Đăng nhập để lưu lịch sử
- Chọn language cụ thể cho accuracy cao hơn
- Review lịch sử để track progress
- Đổi password admin ngay

---

## 🚀 Next Steps

1. **Khám Phá Features:**
   - Try different languages (Python, Java, C++)
   - Analyze AI code vs Human code
   - Check accuracy differences

2. **Xem API Docs:**
   - http://localhost:8000/docs
   - Try các endpoints khác
   - Tích hợp vào app của bạn

3. **Production Deployment:**
   - Setup PostgreSQL
   - Configure .env cho production
   - Use Docker (xem README_V3.md)

---

## 🎉 Hoàn Tất!

Bạn đã sẵn sàng sử dụng GPTSniffer v3.0! 🎊

**Support:**
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Issues: GitHub Issues

**Enjoy detecting AI code! 🤖🔍**

---

**Made with ❤️ by GPTSniffer Team**  
**Version:** 3.0.0  
**Status:** ✅ Production Ready
