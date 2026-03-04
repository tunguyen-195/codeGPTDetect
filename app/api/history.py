"""Analysis history API endpoints"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import (
    AnalysisHistoryResponse,
    AnalysisHistoryList,
    AnalysisUpdate,
    AnalysisStats
)
from app.schemas.response import MessageResponse, SuccessResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=AnalysisHistoryList)
async def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    language: Optional[str] = Query(None),
    prediction: Optional[str] = Query(None),
    is_favorite: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's analysis history
    
    - **skip**: Pagination offset
    - **limit**: Number of items per page
    - **language**: Filter by language
    - **prediction**: Filter by prediction (AI-Generated, Human-Written)
    - **is_favorite**: Filter by favorite status
    """
    analyses = AnalysisService.get_user_analyses(
        db, current_user.id, skip, limit, language, prediction, is_favorite
    )
    
    total = AnalysisService.count_user_analyses(
        db, current_user.id, language, prediction, is_favorite
    )
    
    return AnalysisHistoryList(
        analyses=analyses,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/stats", response_model=AnalysisStats)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's analysis statistics
    """
    stats = AnalysisService.get_user_stats(db, current_user.id)
    
    return AnalysisStats(**stats)


@router.get("/{analysis_id}", response_model=AnalysisHistoryResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get specific analysis by ID
    """
    analysis = AnalysisService.get_analysis_by_id(db, analysis_id, current_user.id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return analysis


@router.put("/{analysis_id}", response_model=AnalysisHistoryResponse)
async def update_analysis(
    analysis_id: int,
    update_data: AnalysisUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update analysis (notes, tags, favorite status)
    """
    analysis = AnalysisService.update_analysis(
        db,
        analysis_id,
        current_user.id,
        update_data.notes,
        update_data.tags,
        update_data.is_favorite
    )
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return analysis


@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete analysis
    """
    success = AnalysisService.delete_analysis(db, analysis_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return MessageResponse(
        message="Analysis deleted successfully"
    )


@router.post("/{analysis_id}/favorite", response_model=SuccessResponse)
async def toggle_favorite(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle favorite status of analysis
    """
    is_favorite = AnalysisService.toggle_favorite(db, analysis_id, current_user.id)
    
    if is_favorite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return SuccessResponse(
        message="Favorite status updated",
        data={"is_favorite": is_favorite}
    )


@router.get("/export/data")
async def export_history(
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export analysis history
    
    - **format**: Export format (json or csv)
    
    TODO: Implement in Phase 4
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Export feature will be implemented in Phase 4"
    )
