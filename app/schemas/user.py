"""User Pydantic schemas"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=1, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=500)
    settings: Optional[dict] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """User schema including hashed password (internal use)"""
    password_hash: str


class UserList(BaseModel):
    """Schema for user list with pagination"""
    users: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class UserStats(BaseModel):
    """User statistics"""
    total_analyses: int
    ai_detected: int
    human_detected: int
    accuracy_rate: float
    favorite_count: int
    languages_used: dict
