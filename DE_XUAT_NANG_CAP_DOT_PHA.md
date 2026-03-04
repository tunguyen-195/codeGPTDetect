# ĐỀ XUẤT NÂNG CẤP ĐỘT PHÁ CHO HỆ THỐNG T07GPTcodeDetect

## 📋 TỔNG QUAN DỰ ÁN HIỆN TẠI

### Điểm mạnh
- ✅ Mô hình CodeBERT đã được fine-tune hiệu quả
- ✅ Web API hoạt động ổn định với FastAPI
- ✅ Giao diện người dùng đẹp, hiện đại
- ✅ Hỗ trợ phát hiện code Java được tạo bởi ChatGPT

### Hạn chế cần khắc phục
- ❌ **Chỉ hoạt động offline**, chưa có tích hợp LMS/GitHub
- ❌ **Không có quản lý người dùng** (giảng viên, sinh viên)
- ❌ **Không lưu trữ lịch sử** phân tích và báo cáo
- ❌ **Thiếu tính năng batch processing** cho nhiều file
- ❌ **Chỉ hỗ trợ Java**, chưa mở rộng ngôn ngữ khác
- ❌ **Không có dashboard analytics** cho giảng viên
- ❌ **Thiếu API tích hợp** với các hệ thống bên ngoài

---

## 🚀 ĐỀ XUẤT 7 MODULE NÂNG CÂP ĐỘT PHÁ

### **MODULE 1: HỆ THỐNG QUẢN LÝ NGƯỜI DÙNG & PHÂN QUYỀN** 🔐

#### Mục tiêu
Xây dựng hệ thống quản lý người dùng đa vai trò để phục vụ môi trường giáo dục

#### Tính năng chi tiết

**1.1. Quản lý vai trò (Role-Based Access Control)**
```
- Admin (Quản trị hệ thống)
  + Quản lý toàn bộ người dùng
  + Xem thống kê toàn trường
  + Cấu hình hệ thống
  
- Giảng viên (Lecturer)
  + Quản lý lớp học và sinh viên
  + Tạo và quản lý bài tập
  + Xem báo cáo chi tiết của sinh viên
  + Thiết lập ngưỡng cảnh báo đạo văn
  
- Sinh viên (Student)
  + Nộp bài tập
  + Xem kết quả phân tích của mình
  + Tự kiểm tra code trước khi nộp
  
- Trợ giảng (Teaching Assistant)
  + Hỗ trợ chấm bài
  + Xem báo cáo lớp
```

**1.2. Tính năng đăng ký và xác thực**
- Đăng nhập qua email trường (@student.hcmute.edu.vn)
- Tích hợp OAuth2.0 (Google, Microsoft)
- Two-Factor Authentication (2FA)
- Single Sign-On (SSO) với hệ thống trường

**1.3. Quản lý hồ sơ**
- Profile cá nhân (avatar, thông tin liên hệ)
- Lịch sử hoạt động
- Thống kê cá nhân

**Công nghệ đề xuất:**
```python
- Backend: FastAPI + JWT Authentication
- Database: PostgreSQL
- ORM: SQLAlchemy
- Password hashing: bcrypt
- Session management: Redis
```

---

### **MODULE 2: HỆ THỐNG QUẢN LÝ BÀI TẬP & LỚP HỌC** 📚

#### Mục tiêu
Tạo môi trường quản lý bài tập lập trình tương tự như Google Classroom

#### Tính năng chi tiết

**2.1. Quản lý lớp học**
```
Giảng viên có thể:
- Tạo lớp học với mã lớp duy nhất
- Mời sinh viên qua email hoặc link
- Thiết lập thời gian học kỳ
- Quản lý danh sách sinh viên (thêm, xóa, chuyển lớp)
- Tạo nhóm sinh viên
```

**2.2. Quản lý bài tập**
```
Giảng viên có thể:
- Tạo bài tập với:
  + Tiêu đề, mô tả chi tiết
  + File đề bài đính kèm
  + Ngôn ngữ lập trình (Java, Python, C++, JavaScript...)
  + Deadline nộp bài
  + Số lần nộp tối đa
  + Cấu hình kiểm tra:
    * Bật/tắt kiểm tra AI-generated
    * Ngưỡng cảnh báo (ví dụ: >70% AI)
    * Kiểm tra similarity code (so sánh giữa sinh viên)
  + Điểm số và tiêu chí chấm
  
- Duplicate bài tập từ kỳ cũ
- Template bài tập có sẵn
- Xuất bài tập ra file PDF/Word
```

**2.3. Nộp bài của sinh viên**
```
Sinh viên có thể:
- Xem danh sách bài tập
- Nộp file code:
  + Single file
  + Multiple files (zip)
  + Link GitHub repository
- Tự kiểm tra trước khi nộp (Pre-submission check)
- Xem lịch sử nộp bài
- Nộp lại nếu còn trong hạn
- Nhận thông báo qua email khi có bài mới
```

**2.4. Tính năng nâng cao**
- Auto-compile và test code
- Plagiarism detection (so sánh code giữa sinh viên)
- Code similarity matrix (heatmap)
- Automatic deadline extension requests

**Công nghệ đề xuất:**
```python
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL với Foreign Keys
- File storage: MinIO / AWS S3
- Task queue: Celery + Redis (xử lý batch)
- Notifications: Firebase Cloud Messaging
```

**Database Schema mẫu:**
```sql
TABLE classes (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  code VARCHAR(50) UNIQUE,
  lecturer_id INTEGER REFERENCES users(id),
  semester VARCHAR(50),
  created_at TIMESTAMP
)

TABLE assignments (
  id SERIAL PRIMARY KEY,
  class_id INTEGER REFERENCES classes(id),
  title VARCHAR(255),
  description TEXT,
  language VARCHAR(50),
  deadline TIMESTAMP,
  max_submissions INTEGER,
  ai_threshold FLOAT,
  enable_ai_check BOOLEAN,
  enable_plagiarism_check BOOLEAN,
  created_at TIMESTAMP
)

TABLE submissions (
  id SERIAL PRIMARY KEY,
  assignment_id INTEGER REFERENCES assignments(id),
  student_id INTEGER REFERENCES users(id),
  file_path TEXT,
  github_url TEXT,
  submitted_at TIMESTAMP,
  ai_score FLOAT,
  ai_label VARCHAR(50),
  plagiarism_score FLOAT,
  status VARCHAR(50) -- pending, analyzed, flagged
)
```

---

### **MODULE 3: PHÂN TÍCH BATCH & XỬ LÝ BẤT ĐỒNG BỘ** ⚡

#### Mục tiêu
Xử lý hàng loạt bài nộp của cả lớp một cách hiệu quả

#### Tính năng chi tiết

**3.1. Batch Upload**
- Upload nhiều file cùng lúc (drag & drop)
- Upload file ZIP chứa nhiều bài
- Import từ GitHub Classroom
- Import từ Google Drive

**3.2. Queue Processing**
```
Khi giảng viên nhấn "Analyze All Submissions":
1. Tạo batch job
2. Đưa vào queue (Celery)
3. Workers xử lý song song:
   - Load model một lần
   - Analyze từng file
   - Lưu kết quả vào database
4. Cập nhật progress bar real-time
5. Gửi notification khi hoàn thành
```

**3.3. Progress Tracking**
- Real-time progress bar
- Estimated time remaining
- Pause/Resume/Cancel job
- Xem log chi tiết

**3.4. Scheduled Analysis**
- Tự động phân tích sau deadline
- Lập lịch phân tích định kỳ
- Cron jobs cho báo cáo tuần/tháng

**Công nghệ đề xuất:**
```python
# Task queue
from celery import Celery
import redis

celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def analyze_submission_batch(submission_ids):
    results = []
    for sid in submission_ids:
        result = analyze_code(sid)
        results.append(result)
        # Update progress
        update_progress(sid, "completed")
    return results

# Real-time updates
from fastapi import WebSocket
import asyncio

@app.websocket("/ws/progress/{job_id}")
async def websocket_progress(websocket: WebSocket, job_id: str):
    await websocket.accept()
    while True:
        progress = get_job_progress(job_id)
        await websocket.send_json(progress)
        await asyncio.sleep(1)
```

---

### **MODULE 4: DASHBOARD ANALYTICS & BÁO CÁO THÔNG MINH** 📊

#### Mục tiêu
Cung cấp insights và visualization cho giảng viên

#### Tính năng chi tiết

**4.1. Dashboard tổng quan**
```
For Giảng viên:
- Tổng số sinh viên trong tất cả lớp
- Tổng số bài tập đã tạo
- Tổng số bài nộp đã phân tích
- Biểu đồ xu hướng AI-generated code theo thời gian
- Top 10 sinh viên có tỷ lệ AI code cao nhất
- Heatmap phân bố AI score trong lớp

For Admin:
- Thống kê toàn trường
- Usage metrics (số lượng API calls, model inference time)
- System health monitoring
```

**4.2. Báo cáo chi tiết theo lớp**
```
Giảng viên chọn lớp → Xem:
1. Distribution Chart:
   - Pie chart: Human vs AI code ratio
   - Histogram: AI score distribution
   - Box plot: Score outliers
   
2. Student Comparison Table:
   - Danh sách sinh viên
   - Số bài nộp
   - Trung bình AI score
   - Số bài bị flag
   - Trend (tăng/giảm)
   
3. Assignment Analytics:
   - Mỗi bài tập: submission rate, average AI score
   - Timeline view
   
4. Anomaly Detection:
   - Sinh viên có sự thay đổi đột ngột (AI score tăng vọt)
   - Patterns đáng ngờ
```

**4.3. Báo cáo chi tiết theo sinh viên**
```
- Profile card với avatar
- Lịch sử nộp bài (timeline view)
- Line chart: AI score qua các bài
- Comparison với trung bình lớp
- Danh sách bài bị cảnh báo
- Comments/Notes từ giảng viên
```

**4.4. Export báo cáo**
- PDF report (auto-generated với charts)
- Excel spreadsheet (raw data)
- JSON/CSV (data export)
- Scheduled email reports

**Công nghệ đề xuất:**
```python
# Visualization
import plotly.express as px
import pandas as pd

# Chart generation
def generate_class_report(class_id):
    df = get_submissions_df(class_id)
    
    # AI Score Distribution
    fig1 = px.histogram(df, x='ai_score', 
                        title='AI Score Distribution',
                        labels={'ai_score': 'AI Confidence'})
    
    # Student Comparison
    fig2 = px.bar(df.groupby('student_name')['ai_score'].mean(),
                  title='Average AI Score by Student')
    
    # Timeline
    fig3 = px.line(df, x='submitted_at', y='ai_score',
                   color='student_name',
                   title='AI Score Trend Over Time')
    
    return {
        'distribution': fig1.to_html(),
        'comparison': fig2.to_html(),
        'timeline': fig3.to_html()
    }

# PDF Export
from weasyprint import HTML
import jinja2

def export_pdf_report(class_id):
    data = generate_class_report(class_id)
    template = jinja2.Template(open('report_template.html').read())
    html = template.render(data)
    pdf = HTML(string=html).write_pdf()
    return pdf
```

---

### **MODULE 5: HỖ TRỢ ĐA NGÔN NGỮ LẬP TRÌNH** 🌐

#### Mục tiêu
Mở rộng từ Java sang các ngôn ngữ phổ biến trong giảng dạy

#### Tính năng chi tiết

**5.1. Ngôn ngữ được hỗ trợ**
```
Priority 1 (Semester 1-2):
- ✅ Java (đã có)
- Python
- C/C++

Priority 2 (Semester 3+):
- JavaScript/TypeScript
- C#
- Go
- Rust
```

**5.2. Multi-model Architecture**
```
Chiến lược:
1. Fine-tune CodeBERT riêng cho mỗi ngôn ngữ
   - codebert-java (hiện tại)
   - codebert-python
   - codebert-cpp
   
2. Hoặc dùng Multi-lingual CodeBERT
   - Fine-tune trên mixed dataset
   - Thêm language_id vào input
   
3. Model Selection:
   - Auto-detect ngôn ngữ từ file extension
   - Cho phép user chọn manually
```

**5.3. Language-specific preprocessing**
```python
class LanguageProcessor:
    def __init__(self, language):
        self.language = language
        self.rules = self.load_rules(language)
    
    def preprocess(self, code):
        if self.language == 'python':
            return self.python_preprocess(code)
        elif self.language == 'java':
            return self.java_preprocess(code)
        # ...
    
    def python_preprocess(self, code):
        # Remove docstrings
        # Handle indentation
        # Remove type hints
        pass
```

**5.4. Dataset Collection**
```
Cần thu thập dataset cho mỗi ngôn ngữ:
- Human-written: GitHub, coding challenges
- AI-generated: Prompt ChatGPT với các bài tập
- Minimum: 1000 samples mỗi ngôn ngữ
```

**Công nghệ đề xuất:**
```python
# Language detection
import pygments.lexers as lexers

def detect_language(code_content, filename):
    # Method 1: From extension
    ext = filename.split('.')[-1]
    lang_map = {
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'js': 'javascript'
    }
    
    # Method 2: Lexer analysis
    try:
        lexer = lexers.guess_lexer(code_content)
        return lexer.name
    except:
        pass
    
    return lang_map.get(ext, 'unknown')

# Multi-model loading
models = {
    'java': load_model('models/codebert-java'),
    'python': load_model('models/codebert-python'),
    'cpp': load_model('models/codebert-cpp')
}

def predict_with_language(code, language):
    model = models[language]
    return model.predict(code)
```

---

### **MODULE 6: TÍCH HỢP HỆ THỐNG BÊN NGOÀI** 🔗

#### Mục tiêu
Kết nối với các nền tảng giáo dục và phát triển phổ biến

#### Tính năng chi tiết

**6.1. GitHub Integration**
```
Tính năng:
- OAuth GitHub login
- Import assignments từ GitHub Classroom
- Auto-analyze khi có commit mới (webhook)
- Clone repository và phân tích
- Comment kết quả trực tiếp vào PR/Issue
- GitHub Actions integration

Workflow:
1. Giảng viên tạo assignment trên GitHub Classroom
2. Liên kết với T07GPTcodeDetect
3. Sinh viên push code lên repo
4. Webhook trigger analysis
5. Kết quả hiển thị trên PR comment
```

**6.2. LMS Integration (Moodle, Canvas)**
```
LTI (Learning Tools Interoperability):
- Embed T07GPTcodeDetect vào Moodle
- Single Sign-On
- Grade passback (đồng bộ điểm)
- Assignment sync
```

**6.3. IDE Extensions**
```
VS Code Extension:
- Right-click code → "Check with T07GPTcodeDetect"
- Real-time analysis trong editor
- Highlight suspicious code blocks
- Suggestions panel

IntelliJ Plugin:
- Tương tự cho Java developers
```

**6.4. REST API mở rộng**
```
Endpoints cho tích hợp:

POST /api/v2/analyze
- Nhận code và return analysis
- API key authentication

POST /api/v2/webhook/github
- Nhận GitHub webhook
- Auto-analyze commits

GET /api/v2/classes/{id}/export
- Export class data
- Support nhiều format

POST /api/v2/bulk-analyze
- Batch analysis
- Async processing
```

**Công nghệ đề xuất:**
```python
# GitHub Integration
from github import Github
import hmac
import hashlib

def verify_github_webhook(request):
    signature = request.headers.get('X-Hub-Signature-256')
    secret = os.getenv('GITHUB_WEBHOOK_SECRET')
    hash = hmac.new(secret.encode(), request.body, hashlib.sha256)
    return hmac.compare_digest(signature, f'sha256={hash.hexdigest()}')

@app.post("/webhook/github")
async def github_webhook(request: Request):
    if not verify_github_webhook(request):
        raise HTTPException(401)
    
    payload = await request.json()
    
    if payload['action'] == 'opened':  # New PR
        repo_url = payload['pull_request']['html_url']
        files = get_changed_files(repo_url)
        results = analyze_files(files)
        post_comment_to_pr(repo_url, results)
    
    return {"status": "ok"}

# LTI Integration
from pylti1p3.contrib.django import DjangoOIDCLogin

@app.post("/lti/login")
def lti_login(request):
    tool_conf = get_lti_config()
    launch_data = DjangoOIDCLogin(request, tool_conf).execute()
    # SSO và lấy thông tin user
    return redirect_to_dashboard()
```

---

### **MODULE 7: EXPLAINABILITY & FEEDBACK** 💡

#### Mục tiêu
Giúp người dùng hiểu tại sao code bị đánh dấu là AI-generated

#### Tính năng chi tiết

**7.1. Code Highlighting**
```
- Highlight các dòng code có "AI signature"
- Hiển thị confidence score cho từng đoạn code
- Color-coded: red (high AI), yellow (medium), green (low AI)
```

**7.2. Explainable AI Features**
```
Phân tích và giải thích:
1. Pattern Detection:
   - "Code này sử dụng naming convention giống ChatGPT"
   - "Comments quá chi tiết và có cấu trúc AI-like"
   - "Error handling pattern điển hình từ AI"
   
2. Statistical Features:
   - Token frequency analysis
   - Code structure similarity
   - Complexity metrics
   
3. Comparison:
   - So sánh với typical human code
   - So sánh với known AI patterns
```

**7.3. Feedback Loop**
```
Sinh viên/Giảng viên có thể:
- Report false positive/negative
- Provide feedback: "This is actually human-written"
- Admin review và label lại
- Re-train model với corrected labels
```

**7.4. Suggestions**
```
Đề xuất cho sinh viên:
- "Để tránh bị phát hiện sai, bạn nên..."
- "Code style của bạn giống AI vì..."
- Educational tips về viết code tự nhiên hơn
```

**Công nghệ đề xuất:**
```python
# Attention Visualization
import torch
from transformers import AutoModel
import matplotlib.pyplot as plt

def visualize_attention(code, model, tokenizer):
    inputs = tokenizer(code, return_tensors='pt')
    outputs = model(**inputs, output_attentions=True)
    
    # Get attention weights from last layer
    attentions = outputs.attentions[-1]  # [batch, heads, seq, seq]
    
    # Average over heads
    avg_attention = attentions.mean(dim=1)[0]  # [seq, seq]
    
    # Plot heatmap
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    plt.figure(figsize=(10, 10))
    plt.imshow(avg_attention.detach().numpy(), cmap='hot')
    plt.xticks(range(len(tokens)), tokens, rotation=90)
    plt.yticks(range(len(tokens)), tokens)
    plt.title('Attention Heatmap')
    return plt

# Feature importance
from lime.lime_text import LimeTextExplainer

def explain_prediction(code, model):
    explainer = LimeTextExplainer(class_names=['ChatGPT', 'Human'])
    
    def predict_proba(texts):
        results = []
        for text in texts:
            pred = model.predict(text)
            results.append([pred['probabilities']['ChatGPT'],
                          pred['probabilities']['Human']])
        return np.array(results)
    
    explanation = explainer.explain_instance(code, predict_proba)
    
    # Return highlighted text with scores
    return {
        'html': explanation.as_html(),
        'features': explanation.as_list()
    }
```

---

## 🏗️ KIẾN TRÚC HỆ THỐNG MỚI

### Tổng quan Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React/Vue.js)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Assignments│  │Analytics│  │Settings  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API / WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                API GATEWAY (FastAPI)                         │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐           │
│  │   Auth     │  │  Classes   │  │ Submissions │           │
│  │ Service    │  │  Service   │  │  Service    │           │
│  └────────────┘  └────────────┘  └─────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                        │
│  ┌─────────────────────────────────────────────────┐        │
│  │           Analysis Engine                        │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │        │
│  │  │CodeBERT  │  │CodeBERT  │  │CodeBERT  │     │        │
│  │  │  Java    │  │ Python   │  │   C++    │     │        │
│  │  └──────────┘  └──────────┘  └──────────┘     │        │
│  └─────────────────────────────────────────────────┘        │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │        Task Queue (Celery + Redis)              │        │
│  │  - Batch processing                             │        │
│  │  - Scheduled jobs                               │        │
│  │  - Email notifications                          │        │
│  └─────────────────────────────────────────────────┘        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  DATA LAYER                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PostgreSQL   │  │  MinIO/S3    │  │    Redis     │      │
│  │  (Metadata)  │  │(File Storage)│  │   (Cache)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack đề xuất

**Frontend:**
```
- Framework: React.js / Vue.js 3
- UI Library: Ant Design / Material-UI
- Charts: Recharts / Chart.js
- State Management: Redux / Pinia
- WebSocket: Socket.io-client
```

**Backend:**
```
- API: FastAPI (Python 3.10+)
- ORM: SQLAlchemy
- Migration: Alembic
- Authentication: JWT + OAuth2
- Task Queue: Celery
- Message Broker: Redis
```

**Database:**
```
- Main DB: PostgreSQL 14+
- Cache: Redis 7+
- File Storage: MinIO / AWS S3
- Search: Elasticsearch (optional)
```

**ML/AI:**
```
- Model: HuggingFace Transformers
- Framework: PyTorch
- Inference: ONNX Runtime (production optimization)
- GPU: CUDA support
```

**Infrastructure:**
```
- Containerization: Docker + Docker Compose
- Orchestration: Kubernetes (production)
- CI/CD: GitHub Actions
- Monitoring: Prometheus + Grafana
- Logging: ELK Stack
```

---

## 📅 LỘ TRÌNH TRIỂN KHAI (ROADMAP)

### Phase 1: Foundation (Tháng 1-2) - **QUAN TRỌNG NHẤT**

**Mục tiêu: Xây dựng nền tảng cơ bản**

**Tuần 1-2: Thiết kế Database & API**
- [ ] Thiết kế ERD database schema
- [ ] Setup PostgreSQL + Redis
- [ ] Migrate mô hình hiện tại sang architecture mới
- [ ] Thiết kế RESTful API spec (OpenAPI/Swagger)

**Tuần 3-4: Module 1 - User Management**
- [ ] Implement User model (Admin, Lecturer, Student)
- [ ] Authentication & Authorization (JWT)
- [ ] Registration & Login API
- [ ] Password reset flow

**Tuần 5-6: Module 2 Part 1 - Class Management**
- [ ] Class CRUD operations
- [ ] Student enrollment
- [ ] Class invitation system

**Tuần 7-8: Module 2 Part 2 - Assignment Management**
- [ ] Assignment CRUD
- [ ] File upload (single & multiple)
- [ ] Submission tracking

**Deliverables:**
- ✅ Working authentication system
- ✅ Basic class & assignment management
- ✅ API documentation

---

### Phase 2: Core Features (Tháng 3-4)

**Mục tiêu: Tích hợp AI analysis vào workflow**

**Tuần 9-10: Module 3 - Batch Processing**
- [ ] Celery task queue setup
- [ ] Batch submission analysis
- [ ] Progress tracking API
- [ ] WebSocket for real-time updates

**Tuần 11-12: Integration with ML Model**
- [ ] Refactor model loading (singleton pattern)
- [ ] Optimize inference speed
- [ ] Add caching mechanism
- [ ] Error handling & retry logic

**Tuần 13-14: Module 4 Part 1 - Basic Dashboard**
- [ ] Overview dashboard
- [ ] Submission list view
- [ ] Basic statistics

**Tuần 15-16: Frontend Development Start**
- [ ] React project setup
- [ ] Login/Register pages
- [ ] Dashboard layout
- [ ] Class & assignment pages

**Deliverables:**
- ✅ Batch analysis working
- ✅ Basic frontend UI
- ✅ End-to-end flow: Create assignment → Submit → Analyze

---

### Phase 3: Advanced Features (Tháng 5-6)

**Mục tiêu: Analytics & Multi-language**

**Tuần 17-18: Module 4 Part 2 - Advanced Analytics**
- [ ] Charts & visualizations (Recharts)
- [ ] Export reports (PDF, Excel)
- [ ] Email notifications
- [ ] Anomaly detection algorithm

**Tuần 19-20: Module 5 - Multi-language Support**
- [ ] Collect Python dataset
- [ ] Fine-tune CodeBERT for Python
- [ ] Language detection
- [ ] Test & evaluate

**Tuần 21-22: Module 7 - Explainability**
- [ ] Attention visualization
- [ ] Code highlighting
- [ ] Feedback mechanism

**Tuần 23-24: Frontend Polish**
- [ ] Improve UX/UI
- [ ] Responsive design
- [ ] Dark mode
- [ ] Accessibility (WCAG)

**Deliverables:**
- ✅ Full analytics dashboard
- ✅ Python support
- ✅ Explainable results
- ✅ Polished UI

---

### Phase 4: Integration & Production (Tháng 7-8)

**Mục tiêu: Tích hợp hệ thống bên ngoài & deploy**

**Tuần 25-26: Module 6 - GitHub Integration**
- [ ] OAuth GitHub
- [ ] Webhook handling
- [ ] Auto-analysis on push
- [ ] PR comments

**Tuần 27-28: Module 6 - LMS Integration**
- [ ] LTI standard implementation
- [ ] Moodle plugin
- [ ] Grade sync

**Tuần 29-30: Production Deployment**
- [ ] Docker containerization
- [ ] Kubernetes setup
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] SSL certificates
- [ ] Domain setup

**Tuần 31-32: Testing & Documentation**
- [ ] Load testing (Locust)
- [ ] Security audit
- [ ] User documentation
- [ ] Video tutorials
- [ ] Admin guide

**Deliverables:**
- ✅ Production-ready system
- ✅ GitHub & LMS integration
- ✅ Complete documentation
- ✅ Deployed website

---

## 📊 KẾ HOẠCH DATASET & TRAINING

### Dataset Collection Strategy

**Java (Đã có):**
- ✅ Existing dataset từ paper
- [ ] Expand với thêm 500 samples

**Python (Priority 1):**
```
Target: 2000 samples (1000 human + 1000 AI)

Human samples:
- LeetCode solutions
- GitHub repositories (educational projects)
- Stack Overflow code snippets
- Student submissions (với consent)

AI samples:
- Prompt ChatGPT với 500 bài tập Python khác nhau
- Variations: với/không comments, với/không docstrings
- Different styles: OOP, functional, procedural
```

**C/C++ (Priority 2):**
```
Target: 1500 samples

Human samples:
- Competitive programming (Codeforces, AtCoder)
- Open-source C projects
- University course assignments

AI samples:
- ChatGPT prompts (algorithms, data structures)
- Focus on: pointers, memory management, STL
```

### Training Plan

**Java Model (Re-training):**
```bash
# Current model: 12 epochs
# Proposed: 15 epochs + larger dataset

python train_model.py \
  --model microsoft/codebert-base \
  --train_data ./datasets/java_extended/train \
  --test_data ./datasets/java_extended/test \
  --epochs 15 \
  --batch_size 32 \
  --learning_rate 5e-5 \
  --output_dir ./models/codebert-java-v2
```

**Python Model (New):**
```bash
python train_model.py \
  --model microsoft/codebert-base \
  --train_data ./datasets/python/train \
  --test_data ./datasets/python/test \
  --epochs 12 \
  --batch_size 32 \
  --learning_rate 5e-5 \
  --output_dir ./models/codebert-python-v1
```

**Evaluation Metrics:**
```
Target thresholds:
- Accuracy: >92%
- Precision: >90%
- Recall: >90%
- F1-Score: >90%
- AUC-ROC: >0.95
```

---

## 💰 ƯỚC TÍNH TÀI NGUYÊN

### Nhân lực

**Development Team (8 tháng):**
```
- 1 Backend Developer (Senior): 8 tháng
- 1 Frontend Developer (Mid-level): 6 tháng
- 1 ML Engineer (Senior): 4 tháng
- 1 UI/UX Designer: 2 tháng
- 1 QA Tester: 3 tháng
- 1 DevOps Engineer: 2 tháng (part-time)
```

### Phần cứng

**Training Server:**
```
- GPU: NVIDIA RTX 3090 / A100 (thuê cloud hoặc mua)
- RAM: 64GB+
- Storage: 1TB SSD
- Estimated cost: $1000-2000/tháng (cloud) hoặc $5000 (mua)
```

**Production Server:**
```
- VM Instance: 8 vCPU, 32GB RAM
- Storage: 500GB SSD
- Bandwidth: 1TB/tháng
- Load Balancer
- Estimated cost: $200-400/tháng
```

### Phần mềm & Tools

```
- GitHub Pro/Team: $4/user/tháng
- Cloud storage (S3/MinIO): $50-100/tháng
- Domain & SSL: $20/năm
- Monitoring tools: $50/tháng
- Total: ~$150-200/tháng
```

---

## 🎯 KẾT QUẢ KỲ VỌNG

### Sau 8 tháng, hệ thống sẽ có:

**✅ Chức năng hoàn chỉnh:**
1. ✔️ Quản lý người dùng đa vai trò
2. ✔️ Quản lý lớp học & bài tập
3. ✔️ Phân tích batch submissions
4. ✔️ Dashboard analytics với charts
5. ✔️ Hỗ trợ Java, Python, C++
6. ✔️ Tích hợp GitHub
7. ✔️ Explainable AI features

**✅ Production-ready:**
- Deployed trên cloud với domain
- HTTPS với SSL
- Load balancer & auto-scaling
- Monitoring & logging
- Backup & disaster recovery

**✅ Documentation đầy đủ:**
- User manual (Sinh viên, Giảng viên, Admin)
- API documentation
- Developer guide
- Video tutorials

**✅ Metrics mục tiêu:**
- Support 100+ giảng viên
- Support 5000+ sinh viên
- Handle 10,000+ submissions/tháng
- API response time < 2s
- Batch analysis: 100 files trong 5 phút
- Uptime: 99.5%

---

## 🔬 HƯỚNG NGHIÊN CỨU TIẾP THEO (FUTURE WORK)

### Research Questions mở rộng

**RQ4: Multi-model AI Detection**
```
Problem: Phát hiện code từ các AI khác nhau (ChatGPT, GitHub Copilot, Claude, Gemini)
Approach:
- Collect datasets từ nhiều AI sources
- Train multi-class classifier
- Compare characteristics của mỗi AI
```

**RQ5: Code Generation Pattern Analysis**
```
Problem: Phân tích patterns đặc trưng của AI-generated code
Approach:
- Extract features: naming conventions, comment styles, error handling
- Cluster analysis
- Create "AI fingerprint" database
```

**RQ6: Cross-language Transfer Learning**
```
Problem: Có thể transfer knowledge từ Java model sang Python không?
Approach:
- Train base model trên multi-language corpus
- Fine-tune cho specific languages
- Measure transfer learning effectiveness
```

**RQ7: Adversarial Robustness**
```
Problem: Sinh viên có thể "trick" hệ thống không?
Approach:
- Adversarial attack testing
- Code obfuscation techniques
- Improve robustness
```

### Advanced Features (Long-term)

**1. AI-assisted Code Review**
```
Không chỉ detect, mà còn:
- Suggest improvements
- Identify bugs/vulnerabilities
- Code quality metrics
- Best practices recommendations
```

**2. Personalized Learning**
```
- Track student progress over time
- Identify learning gaps
- Recommend learning resources
- Adaptive difficulty
```

**3. Collaborative Features**
```
- Peer code review
- Team projects với contribution analysis
- Live coding sessions
- Code comparison tools
```

---

## 📚 TÀI LIỆU THAM KHẢO

### Papers liên quan

1. **GPTSniffer Paper (Base)**
   - Nguyen et al. (2024). Journal of Systems and Software

2. **CodeBERT: A Pre-Trained Model for Programming and Natural Languages**
   - Feng et al. (2020). EMNLP

3. **Detecting AI-Generated Text: A Survey**
   - Multiple surveys on AI detection methods

4. **Plagiarism Detection in Programming Assignments**
   - MOSS, JPlag algorithms

### Tools & Libraries

```
AI/ML:
- transformers (HuggingFace)
- torch (PyTorch)
- scikit-learn
- ONNX

Backend:
- fastapi
- sqlalchemy
- celery
- redis-py

Frontend:
- react
- ant-design / material-ui
- recharts
- axios

DevOps:
- docker
- kubernetes
- nginx
- prometheus
```

---

## 🏆 KẾT LUẬN

Hệ thống **T07GPTcodeDetect** sau khi nâng cấp với 7 modules đề xuất sẽ:

1. ✅ **Giải quyết vấn đề thực tế** trong giảng dạy lập trình
2. ✅ **Tích hợp liền mạch** với quy trình hiện có (GitHub, LMS)
3. ✅ **Mở rộng dễ dàng** (multi-language, new features)
4. ✅ **Production-ready** với monitoring & scaling
5. ✅ **Research-oriented** với metrics và explainability

**Đây không chỉ là một tool phát hiện đạo văn, mà là một nền tảng giáo dục toàn diện**, giúp:
- Giảng viên quản lý lớp học hiệu quả
- Sinh viên học tập đúng đắn và phát triển kỹ năng
- Nhà trường nâng cao chất lượng đào tạo

**Tiềm năng ứng dụng:**
- Sử dụng trong toàn bộ Khoa CNTT&ATTT
- Mở rộng ra các trường khác trong CAND
- Commercialize cho các trường đại học khác
- Publish papers về kết quả triển khai

---

## 📞 THÔNG TIN LIÊN HỆ

**Dự án:** T07GPTcodeDetect  
**Đơn vị:** Khoa Công nghệ và An toàn thông tin  
**Trường:** Đại học Kỹ thuật – Hậu cần CAND  

**Tài liệu này được chuẩn bị bởi:** AI Assistant  
**Ngày:** Tháng 10/2025  
**Phiên bản:** 1.0  

---

**LƯU Ý:** Đây là bản đề xuất chi tiết. Cần review và điều chỉnh theo:
- Ngân sách thực tế
- Nhân lực có sẵn
- Yêu cầu cụ thể của trường
- Timeline linh hoạt

**Bước tiếp theo:**
1. ✅ Review đề xuất này với team
2. ⬜ Chọn modules ưu tiên (recommend: Module 1, 2, 3 trước)
3. ⬜ Xác định ngân sách và nhân lực
4. ⬜ Bắt đầu Phase 1

**Sẵn sàng support:** Có thể cung cấp code template, architecture diagrams, hoặc implementation guides cho bất kỳ module nào!
