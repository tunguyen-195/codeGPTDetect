# T07GPTcodeDetect

> **Hệ thống phát hiện code được sinh bởi các mô hình ngôn ngữ lớn T07**
>
> A deep learning system for detecting AI-generated code using CodeBERT models

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Accuracy](https://img.shields.io/badge/accuracy-100%25%20(Python)-brightgreen.svg)](/)

---

## 📋 Mục Lục

- [Giới Thiệu](#giới-thiệu)
- [Tính Năng](#tính-năng)
- [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Sử Dụng](#sử-dụng)
- [API Documentation](#api-documentation)
- [Mô Hình ML](#mô-hình-ml)
- [Screenshots](#screenshots)
- [Đóng Góp](#đóng-góp)
- [License](#license)

---

## 🎯 Giới Thiệu

**T07GPTcodeDetect** là một hệ thống web application sử dụng deep learning để phát hiện mã nguồn được sinh ra bởi các mô hình AI (như ChatGPT, GPT-4, Copilot, v.v.) và phân biệt với mã nguồn do con người viết.

### Mục Đích

- **Giáo dục**: Giúp giáo viên phát hiện sinh viên sử dụng AI để làm bài tập
- **Code Review**: Hỗ trợ review code để đảm bảo chất lượng
- **Nghiên cứu**: Phân tích patterns của AI-generated code

### Đặc Điểm Nổi Bật

- ✅ **Độ chính xác cao**: 100% trên Python test set, 85% trên Java
- ⚡ **Nhanh chóng**: Phân tích trong < 2 giây
- 🌐 **Đa ngôn ngữ**: Hỗ trợ Python, Java, C++
- 🎨 **Giao diện đẹp**: Modern, responsive UI
- 🔐 **Bảo mật**: JWT authentication, bcrypt password hashing
- 📊 **Thống kê**: Dashboard với charts và analytics

---

## ✨ Tính Năng

### Core Features

#### 🤖 Code Analysis

- Phát hiện code AI-generated vs Human-written
- Hỗ trợ nhiều ngôn ngữ lập trình (Python, Java, C++)
- Auto-detect ngôn ngữ
- Multiple ML models (Python model, Java model, Base model)
- Confidence scoring với probability distribution

#### 👥 User Management

- User registration và authentication
- JWT token-based security
- Role-based access control (Admin/User)
- Session management
- Password hashing với bcrypt

#### 📊 Dashboard & Analytics

- User statistics overview
- Analysis history tracking
- Charts và visualizations
- Export functionality (API ready)

#### 🎨 Modern UI/UX

- Responsive design (mobile/tablet/desktop)
- Beautiful gradient color scheme
- Smooth animations
- Loading states
- Error handling
- Modal dialogs

---

## 🏗️ Kiến Trúc Hệ Thống

### Tech Stack

#### Backend

```
- Python 3.11
- FastAPI (Web framework)
- SQLAlchemy (ORM)
- PyTorch (Deep learning)
- Transformers (Hugging Face)
- JWT (Authentication)
- bcrypt (Password hashing)
- SQLite (Database - dev)
```

#### Frontend

```
- HTML5/CSS3
- Alpine.js (Reactivity)
- Tailwind CSS (Styling)
- Axios (HTTP client)
- CodeMirror (Code editor)
```

#### ML Models

```
- Base: microsoft/codebert-base
- Fine-tuned: Binary classification (AI vs Human)
- Python Model: 100% accuracy
- Java Model: 85% accuracy
```

### Architecture Diagram

```
┌─────────────────────────────────────┐
│         Browser (Client)            │
│  HTML + Alpine.js + Tailwind CSS    │
└──────────────┬──────────────────────┘
               │ HTTP/REST + JWT
               ▼
┌─────────────────────────────────────┐
│      FastAPI Backend Server         │
│  ┌───────────────────────────────┐  │
│  │   Authentication Middleware   │  │
│  │   JWT + Role-based Access     │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │        API Endpoints          │  │
│  │  /api/auth, /api/analysis     │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────┐    ┌──────────────┐
│ Database │    │  ML Models   │
│  SQLite  │    │  CodeBERT    │
│          │    │  Python/Java │
└──────────┘    └──────────────┘
```

---

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 hoặc cao hơn
- 10GB RAM (cho ML models)
- 2GB disk space
- Windows/Linux/macOS

### Bước 1: Clone Repository

```bash
git clone https://github.com/yourusername/T07GPTcodeDetect.git
cd T07GPTcodeDetect
```

### Bước 2: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu Hình Environment

```bash
# Copy template
cp .env.example .env

# Edit .env file và thay đổi:
# - SECRET_KEY
# - JWT_SECRET_KEY  
# - ADMIN_PASSWORD
```

### Bước 4: Khởi Tạo Database

```bash
python scripts/init_db.py
```

### Bước 5: Khởi Động Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Bước 6: Truy Cập

Mở browser và truy cập: **<http://localhost:8000>**

---

## 📖 Sử Dụng

### Quick Start

#### 1. Đăng Nhập

**Admin credentials mặc định:**

```
Email: admin@t07.com
Password: a
```

⚠️ **Lưu ý:** Đổi mật khẩu sau lần đăng nhập đầu tiên!

#### 2. Phân Tích Code

```python
# Paste code này vào editor
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

1. Chọn ngôn ngữ (Python/Java/Auto)
2. Chọn model (Auto/Python/Java)
3. Click "Phân Tích Code"
4. Xem kết quả với confidence score

#### 3. Xem History

- Scroll xuống section "Lịch Sử Gần Đây"
- Xem danh sách các phân tích
- Click để xem chi tiết
- Delete items không cần

---

## 📚 API Documentation

### Authentication

#### Register User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "Password123!",
  "full_name": "Full Name"
}
```

#### Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "Password123!"
}
```

Response:

```json
{
  "access_token": "eyJ0eXAi...",
  "refresh_token": "eyJ0eXAi...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username"
  }
}
```

### Code Analysis

#### Analyze Code

```bash
POST /api/analysis
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "def test(): pass",
  "language": "python",
  "model": "python",
  "save_to_history": true
}
```

Response:

```json
{
  "prediction": "AI-Generated",
  "confidence": 0.9582,
  "probabilities": {
    "AI-Generated": 0.9582,
    "Human-Written": 0.0418
  },
  "language": "python",
  "model_used": "python",
  "execution_time": 127.5
}
```

### Swagger UI

Truy cập API documentation tại: **<http://localhost:8000/docs>**

---

## 🤖 Mô Hình ML

### Training Process

#### Dataset

```
Python Dataset:
- Total samples: 4,152
- AI-generated: 2,152 (52%)
- Human-written: 2,000 (48%)
- Split: 79% train, 21% test

Java Dataset:  
- Legacy dataset from original GPTSniffer paper
```

#### Model Architecture

```
- Base Model: microsoft/codebert-base
- Fine-tuning: Binary classification
- Optimizer: AdamW
- Learning rate: 2e-5
- Epochs: 12 (early stopping at 4)
- Batch size: 16
```

#### Performance

| Model | Language | Accuracy | Precision | Recall | F1-Score |
|-------|----------|----------|-----------|--------|----------|
| Python | Python | 100% | 100% | 100% | 100% |
| Java | Java | ~85% | ~85% | ~85% | ~85% |

#### Model Paths

```
models/
├── python-detector-20251103_135045/  # Python model
└── gptsniffer-finetuned/              # Java model
```

---

## 📸 Screenshots

### Landing Page

![Landing Page](screenshots/landing.png)
*Modern landing page with feature highlights*

### Dashboard

![Dashboard](screenshots/dashboard.png)
*User dashboard with statistics and analysis tool*

### Analysis Results

![Results](screenshots/results.png)
*Code analysis results with confidence scores*

---

## 🗂️ Project Structure

```
T07GPTcodeDetect/
├── app/                        # Backend application
│   ├── main.py                # FastAPI app
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── api/                   # API routes
│   ├── services/              # Business logic
│   ├── core/                  # Security, dependencies
│   └── utils/                 # Utilities
│
├── frontend/                   # Frontend application
│   ├── index.html             # Main HTML
│   └── js/
│       └── app.js             # Alpine.js application
│
├── models/                     # ML models
│   ├── python-detector-*/     # Python model
│   └── gptsniffer-finetuned/  # Java model
│
├── scripts/                    # Utility scripts
│   └── init_db.py             # Database initialization
│
├── .env                        # Environment configuration
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🤝 Đóng Góp

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/T07GPTcodeDetect.git

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run server
python -m uvicorn app.main:app --reload
```

### Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **T07 Team** - *Initial work*

---

## 🙏 Acknowledgments

- Based on the GPTSniffer paper by Nguyen et al.
- CodeBERT model by Microsoft
- Hugging Face Transformers library
- FastAPI framework
- Alpine.js for reactive UI

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🔮 Future Enhancements

- [ ] Support for more languages (JavaScript, Go, Rust)
- [ ] API rate limiting
- [ ] User dashboard improvements
- [ ] Batch processing
- [ ] Export functionality
- [ ] Integration with IDEs
- [ ] Docker deployment
- [ ] Cloud deployment guides

---

**Made with ❤️ by T07 Team**
