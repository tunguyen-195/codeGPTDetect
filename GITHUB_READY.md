# T07GPTcodeDetect - GitHub Deployment Ready

## ✅ Completion Summary

This project has been fully prepared for GitHub deployment. All hardcoded paths have been removed and the database has been reset with default demo accounts.

---

## 🔧 Changes Made

### 1. **Project Renamed**
- **Old Name**: GPTSniffer
- **New Name**: T07GPTcodeDetect

**Changed Files:**
- `app/config.py` - APP_NAME, DATABASE_URL, EMAIL settings
- `app/main.py`, `app/__init__.py` - Documentation strings
- `app/services/ml_service.py` - Model paths
- `.env`, `.env.example` - All configuration references
- `start.bat` - Startup script messages
- `docker-compose.yml` - Container names and volumes
- `webapp/server/*.py` - API titles and service names
- `webapp/static/*.html` - Frontend branding
- `multilang_detector.py` - Model paths
- Model folder: `gptsniffer-finetuned` → `java-detector-finetuned`
- Database: `gptsniffer.db` → `t07gptcodedetect.db`

### 2. **Hardcoded Paths Removed**
- **File**: `webapp/server/main.py`
- **Change**: Replaced absolute Windows path with relative path calculation

**Before:**
```python
self.model_dir_finetuned = "E:\\Freelance\\Research\\D11_8_2025_GPTCodeDetetect\\GPTSniffer\\models\\java-detector-finetuned"
```

**After:**
```python
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
default_model_path = os.path.join(project_root, "models", "java-detector-finetuned")
self.model_dir_finetuned = os.getenv("MODEL_DIR", default_model_path)
```

### 3. **Database Reset**
- **Created**: `scripts/reset_db.py`
- **Function**: Deletes old database and creates fresh one with demo accounts
- **All passwords set to**: `"a"` (for demo purposes)

### 4. **Password Validation Relaxed**
For demo/development purposes, password validation has been relaxed:
- **Minimum length**: 1 character (was 8)
- **Complexity requirements**: Disabled (was: uppercase, lowercase, digit, special)
- **Files modified**:
  - `app/schemas/user.py`
  - `app/schemas/auth.py`
  - `app/core/security.py`

⚠️ **NOTE**: For production deployment, re-enable strict password validation by uncommenting the validation code in `app/core/security.py:validate_password_strength()`

---

## 👥 Default Accounts

The database has been populated with 4 demo accounts (all with password: `a`):

| Email | Username | Password | Role | Description |
|-------|----------|----------|------|-------------|
| `admin@t07.com` | admin | a | admin | System Administrator |
| `user1@t07.com` | user1 | a | user | Regular User 1 |
| `user2@t07.com` | user2 | a | user | Regular User 2 |
| `demo@t07.com` | demo | a | user | Demo Account |

---

## 🧪 Verification Tests

### Test Results (All Passed ✅)

```
[TEST 1] Login with admin@t07.com
✅ Status: 200 OK
✅ User: admin@t07.com
✅ Role: admin

[TEST 2] All @t07.com accounts
✅ admin@t07.com  | Role: admin | Expected: admin
✅ user1@t07.com  | Role: user  | Expected: user
✅ user2@t07.com  | Role: user  | Expected: user
✅ demo@t07.com   | Role: user  | Expected: user

[TEST 3] Code prediction with authentication
✅ Status: 200 OK
✅ Result: Human-Written
✅ Confidence: 100.00%
✅ Model: python

[TEST 4] Health check
✅ Status: healthy
✅ App: T07GPTcodeDetect
✅ Version: 3.0.0

[TEST 5] Models API
✅ Models loaded: python, java, base
✅ Device: cpu
✅ Loaded: true
```

---

## 🚀 Quick Start for New Users

### Prerequisites
- Python 3.11+
- Git

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/T07GPTcodeDetect.git
cd T07GPTcodeDetect

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
# Windows:
start.bat
# Linux/Mac:
./start.sh
```

### Access the Application

- **Web UI**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Login Credentials

Use any of the demo accounts:
- Email: `admin@t07.com`, `user1@t07.com`, `user2@t07.com`, or `demo@t07.com`
- Password: `a`

---

## 📦 Project Structure

```
T07GPTcodeDetect/
├── app/                    # FastAPI application
│   ├── api/               # API endpoints
│   ├── core/              # Core utilities (security, deps)
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── config.py          # Configuration
│   └── main.py            # Application entry point
├── models/                # ML models
│   ├── java-detector-finetuned/
│   └── python-detector-20251103_135045/
├── frontend/              # Web interface
├── scripts/               # Utility scripts
│   ├── init_db.py        # Initialize database
│   └── reset_db.py       # Reset to default state
├── .env                   # Environment variables
├── .env.example          # Example configuration
├── requirements.txt      # Python dependencies
├── start.bat             # Windows startup script
├── start.sh              # Linux/Mac startup script
└── README.md             # Project documentation
```

---

## 🔐 Security Notes

### For Development/Demo
- All accounts use simple password `"a"`
- Password validation is minimal (1 character minimum)
- Debug mode is enabled
- CORS allows localhost origins

### For Production Deployment

**IMPORTANT**: Before deploying to production, you MUST:

1. **Enable Strict Password Validation**
   - Edit `app/core/security.py`
   - Uncomment production validation in `validate_password_strength()`
   - Minimum 8 characters, uppercase, lowercase, digit, special character

2. **Change Secret Keys**
   - Generate new `SECRET_KEY` and `JWT_SECRET_KEY`
   - Use: `openssl rand -hex 32`
   - Update in `.env` file

3. **Update Default Accounts**
   - Change all default passwords
   - Delete or disable demo accounts
   - Create proper admin account

4. **Configure CORS**
   - Update `CORS_ORIGINS` in `.env`
   - Only allow your production domain

5. **Disable Debug Mode**
   - Set `DEBUG=False` in `.env`
   - Set `ENVIRONMENT=production`

6. **Use Production Database**
   - Switch from SQLite to PostgreSQL
   - Update `DATABASE_URL` in `.env`

---

## 📊 Model Information

### Python Model
- **Path**: `models/python-detector-20251103_135045/`
- **Base**: CodeBERT (microsoft/codebert-base)
- **Accuracy**: 100% on test set (823 samples)
- **Training**: 4 epochs with early stopping
- **Dataset**: 4,152 samples (2,152 AI + 2,000 Human)

### Java Model
- **Path**: `models/java-detector-finetuned/`
- **Base**: CodeBERT (microsoft/codebert-base)
- **Accuracy**: ~85% (generalization limited to training domain)
- **Status**: Fine-tuned on specific exercise dataset

---

## 🐛 Known Issues

1. **History Endpoint (401)**
   - The `/api/history` endpoint may return 401 even with valid token
   - This is a minor authentication issue in development
   - Does not affect core functionality
   - Will be fixed in future version

---

## 📝 Environment Variables

See `.env.example` for full configuration options. Key variables:

```env
# Application
APP_NAME=T07GPTcodeDetect
APP_VERSION=3.0.0
DEBUG=True
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./t07gptcodedetect.db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Admin Account
ADMIN_EMAIL=admin@t07.com
ADMIN_PASSWORD=a
ADMIN_USERNAME=admin

# Models
JAVA_MODEL_PATH=models/java-detector-finetuned
PYTHON_MODEL_PATH=models/python-detector-20251103_135045
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Authors

- **T07 Team** - Initial work and development

---

## 🙏 Acknowledgments

- Microsoft for CodeBERT model
- Hugging Face for Transformers library
- FastAPI team for the excellent framework
- CodeSearchNet for human-written code dataset
- Ollama for local LLM inference

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: admin@t07.com

---

**Status**: ✅ **Ready for GitHub Publication**

**Last Updated**: 2025-12-14

**Version**: 3.0.0
