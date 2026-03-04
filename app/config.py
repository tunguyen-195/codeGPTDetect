"""
Application Configuration
Loads settings from environment variables
"""

import os
import json
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "T07GPTcodeDetect"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    JWT_SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12
    
    # Database
    DATABASE_URL: str = "sqlite:///./t07gptcodedetect.db"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Email
    SMTP_ENABLED: bool = False
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@t07gptcodedetect.com"
    EMAIL_FROM_NAME: str = "T07GPTcodeDetect"
    
    # Upload
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    ALLOWED_EXTENSIONS: List[str] = [".py", ".java", ".cpp", ".js", ".ts"]
    UPLOAD_DIR: str = "./uploads"
    
    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v
    
    # Models
    JAVA_MODEL_PATH: str = "models/java-detector-finetuned"
    PYTHON_MODEL_PATH: str = "models/python-detector-finetuned"
    
    # Admin
    ADMIN_EMAIL: str = "admin@t07.com"
    ADMIN_PASSWORD: str = "a"
    ADMIN_USERNAME: str = "admin"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_SIZE: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
