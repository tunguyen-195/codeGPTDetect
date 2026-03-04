"""API Key model"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class APIKey(Base):
    """API Key model for programmatic access"""
    
    __tablename__ = "api_keys"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Key info
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    key_prefix = Column(String(20), nullable=False)  # First 8 chars for display
    
    # Metadata
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Permissions
    permissions = Column(JSON, nullable=True, default=["read"])  # ["read", "write", "admin"]
    rate_limit = Column(Integer, default=100, nullable=False)  # requests per hour
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<APIKey {self.name or self.key_prefix}: User {self.user_id}>"
    
    @property
    def is_expired(self) -> bool:
        """Check if API key is expired"""
        from datetime import datetime
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "key_prefix": self.key_prefix,
            "name": self.name,
            "description": self.description,
            "permissions": self.permissions,
            "rate_limit": self.rate_limit,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired
        }
