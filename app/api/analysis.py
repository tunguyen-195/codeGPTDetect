"""Code analysis API endpoints"""

import time
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user, get_optional_user
from app.services.analysis_service import AnalysisService
from app.services.ml_service import get_ml_service
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.schemas.response import SuccessResponse
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=AnalysisResponse)
async def analyze_code(
    request_data: AnalysisRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Analyze source code for AI detection
    
    - **code**: Source code to analyze
    - **language**: Programming language (auto, python, java, cpp)
    - **model**: Model to use (auto, base, python, java)
    - **save_to_history**: Save result to history (requires authentication)
    - **filename**: Optional filename
    - **notes**: Optional notes
    - **tags**: Optional tags
    """
    start_time = time.time()
    
    # Get ML service
    ml_service = get_ml_service()
    
    # Analyze code using ML service
    try:
        result = ml_service.analyze_code(
            code=request_data.code,
            language=request_data.language,
            model=request_data.model
        )
        
        language = result["language"]
        model = result["model_used"]
        
    except Exception as e:
        logger.error(f"ML analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    
    execution_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Save to history if requested and user is authenticated
    analysis_id = None
    if request_data.save_to_history and current_user:
        analysis = AnalysisService.create_analysis(
            db=db,
            user_id=current_user.id,
            code=request_data.code,
            language=language,
            model_used=model,
            prediction=result["prediction"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            execution_time=execution_time,
            filename=request_data.filename,
            notes=request_data.notes,
            tags=request_data.tags
        )
        analysis_id = analysis.id
    
    return AnalysisResponse(
        prediction=result["prediction"],
        confidence=round(result["confidence"], 4),
        probabilities=result["probabilities"],
        language=language,
        model_used=model,
        execution_time=round(execution_time, 2),
        analysis_id=analysis_id
    )


@router.post("/file", response_model=AnalysisResponse)
async def analyze_file(
    file: UploadFile = File(...),
    language: Optional[str] = "auto",
    model: Optional[str] = "auto",
    save_to_history: bool = True,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Analyze source code from uploaded file
    
    - **file**: Source code file to analyze
    - **language**: Programming language (auto, python, java, cpp)
    - **model**: Model to use (auto, base, python, java)
    - **save_to_history**: Save result to history
    """
    # Read file content
    try:
        content = await file.read()
        code = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Check file size (max 1MB)
    if len(content) > 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too large (max 1MB)"
        )
    
    # Create request
    request_data = AnalysisRequest(
        code=code,
        language=language,
        model=model,
        save_to_history=save_to_history,
        filename=file.filename
    )
    
    # Analyze
    return await analyze_code(request_data, current_user, db)


@router.get("/models", response_model=SuccessResponse)
async def get_available_models():
    """
    Get list of available models
    """
    ml_service = get_ml_service()
    model_info = ml_service.get_model_info()
    
    return SuccessResponse(
        message="Available models",
        data={
            "models": model_info["available_models"],
            "languages": ["python", "java", "cpp"],
            "default_model": "auto",
            "device": model_info["device"],
            "loaded": model_info["loaded"]
        }
    )


@router.post("/detect-language", response_model=SuccessResponse)
async def detect_code_language(code: str):
    """
    Auto-detect programming language from code
    """
    ml_service = get_ml_service()
    language = ml_service.detect_language(code)
    
    return SuccessResponse(
        message="Language detected",
        data={"language": language}
    )
