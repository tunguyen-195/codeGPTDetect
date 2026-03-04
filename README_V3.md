# 🚀 GPTSniffer v3.0 - AI Code Detection Platform

**Full-Stack Web Application với Authentication & Management**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Tổng Quan

GPTSniffer v3.0 là nền tảng web toàn diện để phát hiện code được tạo bởi AI (ChatGPT, GitHub Copilot, v.v.) với độ chính xác cao.

### ✨ Tính Năng Chính

- ✅ **Phát Hiện AI Code** - Accuracy 100% trên Python test set
- ✅ **Đa Ngôn Ngữ** - Hỗ trợ Python, Java, C++
- ✅ **Authentication** - JWT tokens, role-based access
- ✅ **User Management** - Profile, settings, sessions
- ✅ **Analysis History** - Lưu trữ và quản lý kết quả
- ✅ **Dashboard** - Statistics và analytics
- ✅ **Admin Panel** - Quản lý system và users
- ✅ **Modern UI** - Alpine.js + Tailwind CSS
- ✅ **REST API** - Đầy đủ documentation

---

## 🚀 Quick Start

### 1. Cài Đặt Dependencies

```bash
# Clone repository
git clone <your-repo-url>
cd GPTSniffer

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Cấu Hình Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env và set các giá trị:
# - SECRET_KEY (generate với: openssl rand -hex 32)
# - JWT_SECRET_KEY
# - DATABASE_URL (default: sqlite:///./gptsniffer.db)
```

### 3. Initialize Database

```bash
# Run initialization script
python scripts/init_db.py

# Tạo admin user khi được hỏi
# Default: admin@gptsniffer.com / Admin@123
```

### 4. Khởi Động Server

```bash
# Development mode
python -m app.main

# Or với uvicorn
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Truy Cập Application

- **Web UI:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 📚 API Documentation

### Authentication

```bash
# Register
POST /api/auth/register
{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePass123!",
  "full_name": "Full Name"
}

# Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

# Get current user
GET /api/auth/me
Headers: Authorization: Bearer <token>
```

### Code Analysis

```bash
# Analyze code
POST /api/analysis
Headers: Authorization: Bearer <token>
{
  "code": "def hello(): print('Hello')",
  "language": "auto",  # or "python", "java", "cpp"
  "model": "auto",     # or "python", "java", "base"
  "save_to_history": true
}

# Response
{
  "prediction": "AI-Generated",
  "confidence": 0.95,
  "probabilities": {
    "AI-Generated": 0.95,
    "Human-Written": 0.05
  },
  "language": "python",
  "model_used": "python",
  "execution_time": 127.5
}
```

### History

```bash
# Get history
GET /api/history?skip=0&limit=20
Headers: Authorization: Bearer <token>

# Get statistics
GET /api/history/stats
Headers: Authorization: Bearer <token>

# Delete analysis
DELETE /api/history/{id}
Headers: Authorization: Bearer <token>
```

**Full API documentation:** http://localhost:8000/docs

---

## 🏗️ Architecture

### Backend Stack

- **Framework:** FastAPI 0.104
- **Database:** SQLite (dev) / PostgreSQL (prod ready)
- **ORM:** SQLAlchemy 2.0
- **Authentication:** JWT (access + refresh tokens)
- **Security:** bcrypt password hashing
- **ML Models:** CodeBERT (Python, Java models)

### Frontend Stack

- **Framework:** Alpine.js 3.x
- **CSS:** Tailwind CSS
- **HTTP Client:** Axios
- **Charts:** Chart.js
- **Code Editor:** CodeMirror

### Project Structure

```
GPTSniffer/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication
│   │   ├── users.py      # User management
│   │   ├── analysis.py   # Code analysis
│   │   ├── history.py    # Analysis history
│   │   └── admin.py      # Admin endpoints
│   ├── core/             # Core functionality
│   │   ├── security.py   # JWT, passwords
│   │   └── dependencies.py  # FastAPI dependencies
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── analysis.py
│   │   └── ...
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── analysis_service.py
│   │   └── ml_service.py  # ML model integration
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── main.py           # FastAPI app
├── frontend/
│   ├── index.html        # Main page
│   ├── js/app.js         # Alpine.js app
│   └── css/              # Custom styles
├── models/               # ML models
│   ├── python-detector-xxx/
│   └── gptsniffer-finetuned/
├── scripts/
│   └── init_db.py        # Database initialization
├── tests/
│   └── test_api_integration.py
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker config
└── docker-compose.yml    # Docker Compose
```

---

## 🗄️ Database Schema

### Tables

1. **users** - Authentication và profile
   - id, email, username, password_hash
   - role (admin/user/viewer), is_active, is_verified
   - created_at, updated_at, last_login

2. **analysis_history** - Analysis results
   - id, user_id, code, language
   - prediction, confidence, probabilities
   - model_used, execution_time
   - filename, notes, tags, is_favorite

3. **sessions** - JWT token management
   - id, user_id, token, refresh_token
   - ip_address, user_agent
   - created_at, expires_at, is_active

4. **api_keys** - Programmatic access
   - id, user_id, key_hash, key_prefix
   - name, permissions, rate_limit
   - last_used, expires_at

5. **audit_logs** - Security audit trail
   - id, user_id, action, resource
   - details, ip_address, status

---

## 🔒 Security

### Authentication

- **JWT Tokens:** Access token (15min) + Refresh token (7 days)
- **Password:** bcrypt hashing with 12 rounds
- **Session Management:** Database-backed sessions
- **Role-Based Access:** admin, user, viewer roles

### Best Practices

1. **Strong Passwords:** Min 8 chars, uppercase, lowercase, digit
2. **Token Storage:** httpOnly cookies (recommended)
3. **HTTPS Only:** In production
4. **Rate Limiting:** Built-in (configurable)
5. **Input Validation:** Pydantic schemas
6. **SQL Injection:** Protected by SQLAlchemy ORM

---

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
python tests/test_api_integration.py

# Or with pytest
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

- ✅ Authentication (register, login, logout)
- ✅ User management (CRUD, profile)
- ✅ Code analysis (Python, Java, auto-detect)
- ✅ Analysis history (CRUD, stats)
- ✅ Admin endpoints (system stats, users)
- ✅ Security (JWT, permissions, roles)

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build image
docker build -t gptsniffer:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/uploads:/app/uploads \
  --name gptsniffer \
  gptsniffer:latest

# Or use Docker Compose
docker-compose up -d
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📊 Performance

### Metrics (Local machine)

- **API Response Time:** ~100-200ms
- **ML Inference Time:** ~50-150ms (CPU) / ~20-50ms (GPU)
- **Throughput:** ~50-100 requests/second
- **Memory Usage:** ~10GB (with models loaded)
- **Model Accuracy:** 100% on Python test set (823 samples)

### Optimization Tips

1. Use GPU for faster inference
2. Enable caching for repeated analyses
3. Use PostgreSQL for production
4. Add Redis for session storage
5. Use CDN for static assets
6. Enable gzip compression

---

## 🔧 Configuration

### Environment Variables

```bash
# Application
APP_NAME=GPTSniffer
APP_VERSION=3.0.0
DEBUG=True
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite:///./gptsniffer.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/gptsniffer

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Models
JAVA_MODEL_PATH=models/gptsniffer-finetuned
PYTHON_MODEL_PATH=models/python-detector-20251103_135045
```

---

## 📈 Roadmap

### Completed ✅

- [x] Phase 1: Foundation (Database, Auth, API)
- [x] Phase 2: Core Features (ML integration, File upload)
- [x] Phase 3: Frontend (Modern UI, Dashboard)
- [x] Phase 4: Testing & Documentation

### Future Enhancements 🚀

- [ ] Email verification
- [ ] OAuth (Google, GitHub)
- [ ] Batch analysis
- [ ] Export features (CSV, JSON, PDF)
- [ ] Real-time notifications
- [ ] API rate limiting per user
- [ ] Model fine-tuning interface
- [ ] C++ model training
- [ ] Mobile app (Flutter/React Native)
- [ ] Browser extension

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CodeBERT:** Microsoft Research
- **FastAPI:** Sebastián Ramírez
- **Transformers:** Hugging Face
- **Alpine.js:** Caleb Porzio
- **Tailwind CSS:** Adam Wathan

---

## 📞 Support

- **Documentation:** [Full Docs](WEBAPP_UPGRADE_PLAN.md)
- **Issues:** [GitHub Issues](https://github.com/your-repo/issues)
- **Email:** support@gptsniffer.com

---

## 🎉 Credits

**Developed by:** GPTSniffer Team  
**Version:** 3.0.0  
**Release Date:** November 5, 2025  
**Status:** ✅ Production Ready

---

**Made with ❤️ for the AI & Education Community**
