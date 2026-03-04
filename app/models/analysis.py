"""Analysis History model"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AnalysisHistory(Base):
    """Analysis history model - stores all code analysis results"""
    
    __tablename__ = "analysis_history"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Code info
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False, index=True)  # java, python, cpp, etc.
    filename = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    # Analysis results
    model_used = Column(String(50), nullable=False)  # java, python, base
    prediction = Column(String(20), nullable=False, index=True)  # AI-Generated, Human-Written
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON, nullable=True)  # {"AI-Generated": 0.95, "Human-Written": 0.05}
    
    # Performance
    execution_time = Column(Float, nullable=True)  # milliseconds
    
    # User metadata
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True, default=[])  # ["project-x", "homework", etc.]
    is_favorite = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis {self.id}: {self.language} - {self.prediction}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code[:200] + "..." if len(self.code) > 200 else self.code,  # Truncate for preview
            "language": self.language,
            "filename": self.filename,
            "file_size": self.file_size,
            "model_used": self.model_used,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "probabilities": self.probabilities,
            "execution_time": self.execution_time,
            "notes": self.notes,
            "tags": self.tags,
            "is_favorite": self.is_favorite,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def to_dict_full(self):
        """Convert to dictionary with full code"""
        data = self.to_dict()
        data["code"] = self.code  # Full code
        return data
