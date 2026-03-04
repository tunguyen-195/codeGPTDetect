"""
T07GPTcodeDetect v3.0 - Main FastAPI Application
Full-stack AI Code Detection Platform
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
import logging

from app.config import settings
from app.database import Base, engine
from app.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Code Detection Platform - Detect AI-generated vs Human-written code",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Database error occurred",
            "error": str(exc) if settings.DEBUG else "Internal server error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc) if settings.DEBUG else None
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint - Serve frontend
from fastapi.responses import FileResponse

@app.get("/", tags=["Root"], include_in_schema=False)
async def root():
    """
    Serve frontend HTML
    """
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    frontend_file = BASE_DIR / "frontend" / "index.html"
    
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    else:
        # Fallback to API info if frontend not found
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": "AI Code Detection Platform",
            "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
            "health": "/health",
            "api": "/api"
        }


@app.get("/admin", tags=["Admin"], include_in_schema=False)
async def admin_page():
    """
    Serve Admin Panel HTML
    """
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    admin_file = BASE_DIR / "frontend" / "admin.html"
    
    if admin_file.exists():
        return FileResponse(str(admin_file))
    else:
        return {"error": "Admin panel not found"}


# Include API router
app.include_router(api_router, prefix="/api")


# Mount static files (for frontend)
from pathlib import Path
import os

# Get project root directory (parent of app directory)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists() and FRONTEND_DIR.is_dir():
    try:
        app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
        logger.info(f"✅ Frontend mounted from: {FRONTEND_DIR}")
    except Exception as e:
        logger.error(f"❌ Failed to mount frontend: {e}")
else:
    logger.warning(f"⚠️  Frontend directory not found: {FRONTEND_DIR}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
