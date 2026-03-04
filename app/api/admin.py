"""Admin API endpoints"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.core.dependencies import require_role
from app.models.user import User
from app.models.analysis import AnalysisHistory
from app.schemas.response import SuccessResponse

router = APIRouter()


@router.get("/stats", response_model=SuccessResponse, dependencies=[Depends(require_role("admin"))])
async def get_system_stats(
    db: Session = Depends(get_db)
):
    """
    Get system statistics (Admin only)
    
    - Total users, active users
    - Total analyses
    - AI vs Human detection stats
    - Language breakdown
    """
    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    verified_users = db.query(func.count(User.id)).filter(User.is_verified == True).scalar()
    
    # Analysis stats
    total_analyses = db.query(func.count(AnalysisHistory.id)).scalar()
    ai_detected = db.query(func.count(AnalysisHistory.id)).filter(
        AnalysisHistory.prediction == "AI-Generated"
    ).scalar()
    human_detected = total_analyses - ai_detected if total_analyses else 0
    
    # Language breakdown
    language_stats = db.query(
        AnalysisHistory.language,
        func.count(AnalysisHistory.id).label('count')
    ).group_by(AnalysisHistory.language).all()
    
    by_language = {lang: count for lang, count in language_stats}
    
    # Average confidence
    avg_confidence = db.query(func.avg(AnalysisHistory.confidence)).scalar() or 0.0
    
    return SuccessResponse(
        message="System statistics",
        data={
            "users": {
                "total": total_users,
                "active": active_users,
                "verified": verified_users,
                "inactive": total_users - active_users
            },
            "analyses": {
                "total": total_analyses,
                "ai_generated": ai_detected,
                "human_written": human_detected,
                "by_language": by_language,
                "avg_confidence": round(avg_confidence, 2)
            }
        }
    )


@router.get("/users/recent", response_model=SuccessResponse, dependencies=[Depends(require_role("admin"))])
async def get_recent_users(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recently registered users (Admin only)
    """
    from sqlalchemy import desc
    
    users = db.query(User).order_by(desc(User.created_at)).limit(limit).all()
    
    return SuccessResponse(
        message="Recent users",
        data={
            "users": [
                {
                    "id": u.id,
                    "email": u.email,
                    "username": u.username,
                    "role": u.role,
                    "is_active": u.is_active,
                    "created_at": u.created_at.isoformat()
                }
                for u in users
            ]
        }
    )


@router.get("/analyses/recent", response_model=SuccessResponse, dependencies=[Depends(require_role("admin"))])
async def get_recent_analyses(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recent analyses (Admin only)
    """
    from sqlalchemy import desc
    
    analyses = db.query(AnalysisHistory).order_by(desc(AnalysisHistory.created_at)).limit(limit).all()
    
    return SuccessResponse(
        message="Recent analyses",
        data={
            "analyses": [
                {
                    "id": a.id,
                    "user_id": a.user_id,
                    "language": a.language,
                    "prediction": a.prediction,
                    "confidence": round(a.confidence, 2),
                    "created_at": a.created_at.isoformat()
                }
                for a in analyses
            ]
        }
    )


@router.get("/health", response_model=SuccessResponse)
async def health_check(
    db: Session = Depends(get_db)
):
    """
    System health check
    """
    # Check database connection
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return SuccessResponse(
        message="System health check",
        data={
            "status": "healthy" if db_status == "healthy" else "degraded",
            "database": db_status,
            "version": "3.0.0"
        }
    )
