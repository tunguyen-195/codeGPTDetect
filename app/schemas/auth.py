"""Authentication Pydantic schemas"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class LoginRequest(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str


class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordChangeRequest(BaseModel):
    """Schema for password change"""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class EmailVerificationRequest(BaseModel):
    """Schema for email verification"""
    token: str
