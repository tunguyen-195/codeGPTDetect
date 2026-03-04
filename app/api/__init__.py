"""API routes"""

from fastapi import APIRouter

from app.api import auth, users, analysis, history, admin

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(history.router, prefix="/history", tags=["History"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])

__all__ = ["api_router"]
