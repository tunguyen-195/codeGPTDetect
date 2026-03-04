# HƯỚNG DẪN TRIỂN KHAI MODULE 1: USER MANAGEMENT & AUTHENTICATION

## 🎯 Mục tiêu
Xây dựng hệ thống quản lý người dùng với authentication và phân quyền cho T07GPTcodeDetect

## 📋 Yêu cầu
- Python 3.10+
- PostgreSQL 14+
- Redis 7+
- Kiến thức về FastAPI, SQLAlchemy, JWT

---

## BƯỚC 1: CÀI ĐẶT DEPENDENCIES

### 1.1. Tạo file requirements_module1.txt

```txt
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1
python-dotenv==1.0.0

# Redis & Session
redis==5.0.1
aioredis==2.0.1

# Email
fastapi-mail==1.4.1

# Validation
pydantic==2.5.0
pydantic-settings==2.1.0
email-validator==2.1.0
```

### 1.2. Cài đặt

```bash
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements_module1.txt
```

---

## BƯỚC 2: CẤU HÌNH DATABASE

### 2.1. Cài đặt PostgreSQL

**Windows:**
```bash
# Download từ: https://www.postgresql.org/download/windows/
# Hoặc dùng Docker:
docker run --name postgres-t07 ^
  -e POSTGRES_PASSWORD=yourpassword ^
  -e POSTGRES_DB=t07gptdetect ^
  -p 5432:5432 ^
  -d postgres:14
```

### 2.2. Tạo database

```sql
-- Kết nối PostgreSQL
psql -U postgres

-- Tạo database
CREATE DATABASE t07gptdetect;
CREATE USER t07admin WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE t07gptdetect TO t07admin;
```

### 2.3. Cài đặt Redis

```bash
# Windows: Download từ https://redis.io/download
# Hoặc Docker:
docker run --name redis-t07 -p 6379:6379 -d redis:7
```

---

## BƯỚC 3: CẤU TRÚC DỰ ÁN MỚI

### 3.1. Tạo structure

```
GPTSniffer/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   │
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── base.py
│   │
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   │
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── deps.py           # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       └── users.py
│   │
│   ├── core/                  # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py       # Password hashing, JWT
│   │   └── config.py
│   │
│   └── services/              # Business logic
│       ├── __init__.py
│       └── user_service.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   └── env.py
│
├── .env                       # Environment variables
├── alembic.ini               # Alembic config
└── requirements_module1.txt
```

### 3.2. Tạo folders

```bash
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
mkdir app
mkdir app\models app\schemas app\api app\api\v1 app\core app\services
mkdir alembic alembic\versions

# Tạo __init__.py files
echo. > app\__init__.py
echo. > app\models\__init__.py
echo. > app\schemas\__init__.py
echo. > app\api\__init__.py
echo. > app\api\v1\__init__.py
echo. > app\core\__init__.py
echo. > app\services\__init__.py
```

---

## BƯỚC 4: CONFIGURATION

### 4.1. Tạo file .env

```env
# Database
DATABASE_URL=postgresql+asyncpg://t07admin:your_secure_password@localhost:5432/t07gptdetect

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# App
APP_NAME=T07GPTcodeDetect
API_V1_PREFIX=/api/v1
DEBUG=True
```

### 4.2. Tạo app/core/config.py

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "T07GPTcodeDetect"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

---

## BƯỚC 5: DATABASE MODELS

### 5.1. Tạo app/database.py

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### 5.2. Tạo app/models/user.py

```python
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LECTURER = "lecturer"
    STUDENT = "student"
    TA = "ta"  # Teaching Assistant

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Profile
    student_id = Column(String(20), unique=True, nullable=True)  # For students
    department = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
```

---

## BƯỚC 6: PYDANTIC SCHEMAS

### 6.1. Tạo app/schemas/user.py

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

# Base schema
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    role: UserRole = UserRole.STUDENT

# Schema for user registration
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    student_id: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=255)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

# Schema for user update
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    department: Optional[str] = Field(None, max_length=255)
    avatar_url: Optional[str] = None

# Schema for password change
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

# Schema for response
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    student_id: Optional[str] = None
    department: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for user list (limited info)
class UserListResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True
```

### 6.2. Tạo app/schemas/token.py

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int] = None  # user_id
    exp: Optional[int] = None
    
class RefreshToken(BaseModel):
    refresh_token: str
```

---

## BƯỚC 7: SECURITY & AUTHENTICATION

### 7.1. Tạo app/core/security.py

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## BƯỚC 8: API DEPENDENCIES

### 8.1. Tạo app/api/deps.py

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User, UserRole
from app.core.security import decode_token
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Role-based dependencies
async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def require_lecturer(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require lecturer or admin role"""
    if current_user.role not in [UserRole.LECTURER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

---

## BƯỚC 9: USER SERVICE

### 9.1. Tạo app/services/user_service.py

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    """User service for business logic"""
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create new user"""
        # Check if user exists
        existing_user = await UserService.get_user_by_email(db, user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user
        db_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role,
            student_id=user_data.student_id,
            department=user_data.department
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession, 
        email: str, 
        password: str
    ) -> Optional[User]:
        """Authenticate user"""
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> User:
        """Update user"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Update fields
        if user_data.full_name:
            user.full_name = user_data.full_name
        if user_data.department:
            user.department = user_data.department
        if user_data.avatar_url:
            user.avatar_url = user_data.avatar_url
        
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def change_password(
        db: AsyncSession,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change user password"""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            raise ValueError("Incorrect password")
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        await db.commit()
        
        return True
    
    @staticmethod
    async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None
    ) -> List[User]:
        """Get list of users"""
        query = select(User)
        
        if role:
            query = query.where(User.role == role)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        
        return result.scalars().all()
```

---

## BƯỚC 10: API ENDPOINTS

### 10.1. Tạo app/api/v1/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, RefreshToken
from app.services.user_service import UserService
from app.core.security import create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Đăng ký tài khoản mới
    
    - **email**: Email hợp lệ (@student.hcmute.edu.vn hoặc @hcmute.edu.vn)
    - **password**: Tối thiểu 8 ký tự, bao gồm chữ hoa, chữ thường và số
    - **full_name**: Họ và tên đầy đủ
    - **role**: Vai trò (student, lecturer, admin)
    """
    try:
        user = await UserService.create_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Đăng nhập vào hệ thống
    
    - **username**: Email đăng ký
    - **password**: Mật khẩu
    
    Returns access_token và refresh_token
    """
    user = await UserService.authenticate_user(
        db, 
        email=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshToken,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token bằng refresh token
    """
    payload = decode_token(refresh_data.refresh_token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = await UserService.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
```

### 10.2. Tạo app/api/v1/users.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate, PasswordChange, UserListResponse
from app.services.user_service import UserService
from app.api.deps import get_current_active_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Lấy thông tin user hiện tại
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cập nhật thông tin user hiện tại
    """
    try:
        updated_user = await UserService.update_user(db, current_user.id, user_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/me/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Đổi mật khẩu
    """
    try:
        await UserService.change_password(
            db,
            current_user.id,
            password_data.old_password,
            password_data.new_password
        )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserListResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: UserRole = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Lấy danh sách users (Admin only)
    """
    users = await UserService.get_users(db, skip=skip, limit=limit, role=role)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Lấy thông tin user theo ID (Admin only)
    """
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## BƯỚC 11: MAIN APP

### 11.1. Tạo app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API cho hệ thống phát hiện code AI T07GPTcodeDetect",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "T07GPTcodeDetect API",
        "version": "2.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## BƯỚC 12: DATABASE MIGRATION

### 12.1. Setup Alembic

```bash
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
alembic init alembic
```

### 12.2. Cấu hình alembic.ini

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql+asyncpg://t07admin:your_secure_password@localhost:5432/t07gptdetect
```

### 12.3. Cấu hình alembic/env.py

```python
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio

# Import your models
from app.database import Base
from app.models.user import User  # Import all models here

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 12.4. Tạo migration

```bash
# Tạo migration file
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head
```

---

## BƯỚC 13: CHẠY THỬ

### 13.1. Start server

```bash
cd E:\Freelance\Research\D11_8_2025_GPTCodeDetetect\GPTSniffer
.\.venv\Scripts\activate

# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 13.2. Test API

Truy cập: http://localhost:8000/api/docs

**Test flow:**

1. **Register user:**
```json
POST /api/v1/auth/register
{
  "email": "lecturer@hcmute.edu.vn",
  "password": "SecurePass123",
  "full_name": "Nguyễn Văn A",
  "role": "lecturer",
  "department": "Khoa CNTT&ATTT"
}
```

2. **Login:**
```json
POST /api/v1/auth/login
{
  "username": "lecturer@hcmute.edu.vn",
  "password": "SecurePass123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

3. **Get current user:**
```
GET /api/v1/users/me
Authorization: Bearer eyJ...
```

---

## BƯỚC 14: TẠO ADMIN USER

### 14.1. Tạo script create_admin.py

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

async def create_admin():
    async with AsyncSessionLocal() as db:
        # Check if admin exists
        admin = await db.execute(
            select(User).where(User.email == "admin@hcmute.edu.vn")
        )
        
        if admin.scalar_one_or_none():
            print("Admin already exists")
            return
        
        # Create admin
        admin_user = User(
            email="admin@hcmute.edu.vn",
            full_name="System Administrator",
            hashed_password=get_password_hash("Admin@123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        
        db.add(admin_user)
        await db.commit()
        
        print("Admin created successfully!")
        print("Email: admin@hcmute.edu.vn")
        print("Password: Admin@123")

if __name__ == "__main__":
    asyncio.run(create_admin())
```

```bash
python create_admin.py
```

---

## ✅ HOÀN THÀNH MODULE 1!

Bây giờ bạn đã có:
- ✅ User authentication với JWT
- ✅ Role-based access control
- ✅ Password hashing an toàn
- ✅ User management APIs
- ✅ Database với PostgreSQL
- ✅ API documentation tự động (Swagger)

**Bước tiếp theo:**
- Module 2: Class & Assignment Management
- Tích hợp với ML model hiện tại
- Frontend development

**Hỗ trợ:**
Nếu gặp lỗi, kiểm tra:
1. PostgreSQL và Redis đang chạy
2. .env file đúng cấu hình
3. Database migrations đã chạy
4. Dependencies đã install đầy đủ
