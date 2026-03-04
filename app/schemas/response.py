"""Generic response schemas"""

from typing import Any, Optional, List
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    success: bool = False
    message: str
    error: Optional[str] = None
    details: Optional[dict] = None


class MessageResponse(BaseModel):
    """Simple message response"""
    message: str


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    database: str
    models_loaded: dict
    uptime: Optional[float] = None
