"""User service - Business logic for user operations"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class UserService:
    """Service class for user operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """Get list of users with filters"""
        query = db.query(User)
        
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def count_users(
        db: Session,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """Count users with filters"""
        query = db.query(func.count(User.id))
        
        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.scalar()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create new user"""
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user object
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=password_hash,
            full_name=user_data.full_name,
            role="user",  # Default role
            is_active=True,
            is_verified=False  # Require email verification
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Update fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        
        return True
    
    @staticmethod
    def verify_user_email(db: Session, user_id: int) -> bool:
        """Mark user email as verified"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.is_verified = True
        db.commit()
        
        return True
    
    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Verify old password
        if not verify_password(old_password, user.password_hash):
            return False
        
        # Set new password
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
        return True
    
    @staticmethod
    def update_role(db: Session, user_id: int, new_role: str) -> Optional[User]:
        """Update user role (admin only)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        user.role = new_role
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def toggle_active_status(db: Session, user_id: int) -> Optional[User]:
        """Toggle user active status"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def update_last_login(db: Session, user_id: int):
        """Update user's last login timestamp"""
        from datetime import datetime
        
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login = datetime.now()
            db.commit()
