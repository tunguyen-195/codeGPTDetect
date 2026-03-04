"""Authentication service - Business logic for authentication"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.session import Session as UserSession
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.config import settings


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        
        Returns:
            User object if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def create_session(
        db: Session,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create new session for user and generate tokens
        
        Returns:
            Dictionary with access_token, refresh_token, and expiration info
        """
        # Generate tokens
        access_token = create_access_token(data={"sub": user_id})
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        # Calculate expiration
        expires_at = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Create session record
        session = UserSession(
            user_id=user_id,
            token=access_token,
            refresh_token=refresh_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            is_active=True
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Refresh access token using refresh token
        
        Returns:
            Dictionary with new access_token, or None if invalid
        """
        # Decode refresh token
        payload = decode_token(refresh_token)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        # Verify session exists and is active
        session = db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now()
        ).first()
        
        if not session:
            return None
        
        # Generate new access token
        access_token = create_access_token(data={"sub": user_id})
        
        # Update session
        session.token = access_token
        db.commit()
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    @staticmethod
    def logout(db: Session, user_id: int, token: str) -> bool:
        """
        Logout user by invalidating session
        
        Returns:
            True if logout successful, False otherwise
        """
        session = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.token == token,
            UserSession.is_active == True
        ).first()
        
        if not session:
            return False
        
        session.is_active = False
        db.commit()
        
        return True
    
    @staticmethod
    def logout_all_sessions(db: Session, user_id: int) -> int:
        """
        Logout user from all sessions
        
        Returns:
            Number of sessions invalidated
        """
        count = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).update({"is_active": False})
        
        db.commit()
        
        return count
    
    @staticmethod
    def get_active_sessions(db: Session, user_id: int):
        """Get all active sessions for user"""
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now()
        ).all()
    
    @staticmethod
    def cleanup_expired_sessions(db: Session) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions deleted
        """
        count = db.query(UserSession).filter(
            UserSession.expires_at < datetime.now()
        ).delete()
        
        db.commit()
        
        return count
    
    @staticmethod
    def verify_session(db: Session, token: str) -> Optional[UserSession]:
        """Verify if session is valid"""
        return db.query(UserSession).filter(
            UserSession.token == token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now()
        ).first()
