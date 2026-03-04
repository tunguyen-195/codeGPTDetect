"""Authentication API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordChangeRequest
)
from app.schemas.user import UserResponse
from app.schemas.response import SuccessResponse, MessageResponse
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **username**: Unique username (3-50 chars)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **full_name**: Optional full name
    """
    # Check if email exists
    if UserService.get_user_by_email(db, request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if UserService.get_user_by_username(db, request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = UserService.create_user(db, request)
    
    return SuccessResponse(
        message="User registered successfully",
        data={
            "id": user.id,
            "email": user.email,
            "username": user.username
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request_data: LoginRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    Returns JWT access token and refresh token
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, request_data.email, request_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Get client info
    ip_address = req.client.host if req.client else None
    user_agent = req.headers.get("user-agent")
    
    # Create session and tokens
    tokens = AuthService.create_session(db, user.id, ip_address, user_agent)
    
    # Update last login
    UserService.update_last_login(db, user.id)
    
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"],
        expires_in=tokens["expires_in"],
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_verified": user.is_verified
        }
    )


@router.post("/refresh", response_model=SuccessResponse)
async def refresh_token(
    request_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    tokens = AuthService.refresh_access_token(db, request_data.refresh_token)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    return SuccessResponse(
        message="Token refreshed successfully",
        data=tokens
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout current user
    
    Invalidates current session
    """
    # Note: In real implementation, we'd get the actual token from the request
    # For now, we'll logout all sessions
    count = AuthService.logout_all_sessions(db, current_user.id)
    
    return MessageResponse(
        message=f"Logged out successfully from {count} session(s)"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return current_user


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password
    """
    success = UserService.change_password(
        db,
        current_user.id,
        request_data.old_password,
        request_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    return MessageResponse(
        message="Password changed successfully"
    )


@router.get("/sessions")
async def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all active sessions for current user
    """
    sessions = AuthService.get_active_sessions(db, current_user.id)
    
    return SuccessResponse(
        message="Active sessions retrieved",
        data={
            "total": len(sessions),
            "sessions": [
                {
                    "id": s.id,
                    "ip_address": s.ip_address,
                    "user_agent": s.user_agent,
                    "created_at": s.created_at.isoformat(),
                    "expires_at": s.expires_at.isoformat()
                }
                for s in sessions
            ]
        }
    )
