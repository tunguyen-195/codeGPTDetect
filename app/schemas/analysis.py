"""Analysis Pydantic schemas"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Schema for code analysis request"""
    code: str = Field(..., min_length=1, max_length=100000)
    language: Optional[str] = Field("auto", description="Language: auto, python, java, cpp")
    model: Optional[str] = Field("auto", description="Model: auto, base, python, java")
    save_to_history: bool = Field(True, description="Save analysis to history")
    filename: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(None, max_items=10)


class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    prediction: str
    confidence: float
    probabilities: dict
    language: str
    model_used: str
    execution_time: float
    analysis_id: Optional[int] = None
    message: str = "Analysis completed successfully"


class AnalysisHistoryResponse(BaseModel):
    """Schema for analysis history item"""
    id: int
    code: str
    language: str
    model_used: str
    prediction: str
    confidence: float
    probabilities: dict
    execution_time: Optional[float]
    created_at: datetime
    filename: Optional[str]
    file_size: Optional[int]
    notes: Optional[str]
    is_favorite: bool
    tags: Optional[dict]
    
    class Config:
        from_attributes = True


class AnalysisHistoryList(BaseModel):
    """Schema for paginated analysis history"""
    analyses: List[AnalysisHistoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AnalysisStats(BaseModel):
    """Schema for analysis statistics"""
    total_analyses: int
    ai_generated: int
    human_written: int
    by_language: dict
    by_model: dict
    avg_confidence: float
    favorite_count: int


class AnalysisUpdate(BaseModel):
    """Schema for updating analysis"""
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(None, max_items=10)
    is_favorite: Optional[bool] = None


class AnalysisExport(BaseModel):
    """Schema for exporting analysis data"""
    format: str = Field("json", description="Export format: json, csv")
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    language: Optional[str] = None
    prediction: Optional[str] = None
