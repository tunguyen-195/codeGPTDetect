"""Audit Log model"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    """Audit log model for tracking user actions"""
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign key (nullable - can log system actions)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Action info
    action = Column(String(50), nullable=False, index=True)  # login, logout, analysis, update_user, etc.
    resource_type = Column(String(50), nullable=True)  # user, analysis, settings, etc.
    resource_id = Column(Integer, nullable=True)
    
    # Details
    details = Column(JSON, nullable=True)
    
    # Request info
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Status
    status = Column(String(20), nullable=False)  # success, failure, error
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    def __repr__(self):
        return f"<AuditLog {self.id}: {self.action} by User {self.user_id}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "ip_address": self.ip_address,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
