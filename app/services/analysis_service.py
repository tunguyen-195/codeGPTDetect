"""Analysis service - Business logic for code analysis"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.analysis import AnalysisHistory
from app.models.user import User


class AnalysisService:
    """Service class for analysis operations"""
    
    @staticmethod
    def create_analysis(
        db: Session,
        user_id: int,
        code: str,
        language: str,
        model_used: str,
        prediction: str,
        confidence: float,
        probabilities: dict,
        execution_time: float,
        filename: Optional[str] = None,
        notes: Optional[str] = None,
        tags: Optional[list] = None
    ) -> AnalysisHistory:
        """
        Save analysis result to database
        
        Args:
            db: Database session
            user_id: User ID
            code: Source code
            language: Programming language
            model_used: ML model used
            prediction: Prediction result
            confidence: Confidence score
            probabilities: Prediction probabilities
            execution_time: Time taken for analysis
            filename: Optional filename
            notes: Optional user notes
            tags: Optional tags list
            
        Returns:
            Created AnalysisHistory object
        """
        analysis = AnalysisHistory(
            user_id=user_id,
            code=code,
            language=language,
            model_used=model_used,
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities,
            execution_time=execution_time,
            filename=filename,
            file_size=len(code.encode('utf-8')),
            notes=notes,
            tags={"tags": tags} if tags else None
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    @staticmethod
    def get_analysis_by_id(db: Session, analysis_id: int, user_id: int) -> Optional[AnalysisHistory]:
        """Get analysis by ID (user can only access their own analyses)"""
        return db.query(AnalysisHistory).filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == user_id
        ).first()
    
    @staticmethod
    def get_user_analyses(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        language: Optional[str] = None,
        prediction: Optional[str] = None,
        is_favorite: Optional[bool] = None
    ) -> List[AnalysisHistory]:
        """
        Get user's analysis history with filters
        
        Args:
            db: Database session
            user_id: User ID
            skip: Offset for pagination
            limit: Limit for pagination
            language: Filter by language
            prediction: Filter by prediction
            is_favorite: Filter by favorite status
            
        Returns:
            List of AnalysisHistory objects
        """
        query = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == user_id)
        
        if language:
            query = query.filter(AnalysisHistory.language == language)
        if prediction:
            query = query.filter(AnalysisHistory.prediction == prediction)
        if is_favorite is not None:
            query = query.filter(AnalysisHistory.is_favorite == is_favorite)
        
        return query.order_by(desc(AnalysisHistory.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_user_analyses(
        db: Session,
        user_id: int,
        language: Optional[str] = None,
        prediction: Optional[str] = None,
        is_favorite: Optional[bool] = None
    ) -> int:
        """Count user's analyses with filters"""
        query = db.query(func.count(AnalysisHistory.id)).filter(
            AnalysisHistory.user_id == user_id
        )
        
        if language:
            query = query.filter(AnalysisHistory.language == language)
        if prediction:
            query = query.filter(AnalysisHistory.prediction == prediction)
        if is_favorite is not None:
            query = query.filter(AnalysisHistory.is_favorite == is_favorite)
        
        return query.scalar()
    
    @staticmethod
    def update_analysis(
        db: Session,
        analysis_id: int,
        user_id: int,
        notes: Optional[str] = None,
        tags: Optional[list] = None,
        is_favorite: Optional[bool] = None
    ) -> Optional[AnalysisHistory]:
        """
        Update analysis notes, tags, or favorite status
        
        Args:
            db: Database session
            analysis_id: Analysis ID
            user_id: User ID (for permission check)
            notes: Optional notes to update
            tags: Optional tags to update
            is_favorite: Optional favorite status to update
            
        Returns:
            Updated AnalysisHistory object or None
        """
        analysis = db.query(AnalysisHistory).filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == user_id
        ).first()
        
        if not analysis:
            return None
        
        if notes is not None:
            analysis.notes = notes
        if tags is not None:
            analysis.tags = {"tags": tags}
        if is_favorite is not None:
            analysis.is_favorite = is_favorite
        
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    @staticmethod
    def delete_analysis(db: Session, analysis_id: int, user_id: int) -> bool:
        """
        Delete analysis
        
        Args:
            db: Database session
            analysis_id: Analysis ID
            user_id: User ID (for permission check)
            
        Returns:
            True if deleted, False if not found
        """
        analysis = db.query(AnalysisHistory).filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == user_id
        ).first()
        
        if not analysis:
            return False
        
        db.delete(analysis)
        db.commit()
        
        return True
    
    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get user's analysis statistics
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with statistics
        """
        # Total analyses
        total = db.query(func.count(AnalysisHistory.id)).filter(
            AnalysisHistory.user_id == user_id
        ).scalar()
        
        # AI vs Human
        ai_count = db.query(func.count(AnalysisHistory.id)).filter(
            AnalysisHistory.user_id == user_id,
            AnalysisHistory.prediction == "AI-Generated"
        ).scalar()
        
        human_count = total - ai_count
        
        # By language
        language_stats = db.query(
            AnalysisHistory.language,
            func.count(AnalysisHistory.id).label('count')
        ).filter(
            AnalysisHistory.user_id == user_id
        ).group_by(AnalysisHistory.language).all()
        
        by_language = {lang: count for lang, count in language_stats}
        
        # By model
        model_stats = db.query(
            AnalysisHistory.model_used,
            func.count(AnalysisHistory.id).label('count')
        ).filter(
            AnalysisHistory.user_id == user_id
        ).group_by(AnalysisHistory.model_used).all()
        
        by_model = {model: count for model, count in model_stats}
        
        # Average confidence
        avg_confidence = db.query(
            func.avg(AnalysisHistory.confidence)
        ).filter(
            AnalysisHistory.user_id == user_id
        ).scalar() or 0.0
        
        # Favorites
        favorites = db.query(func.count(AnalysisHistory.id)).filter(
            AnalysisHistory.user_id == user_id,
            AnalysisHistory.is_favorite == True
        ).scalar()
        
        return {
            "total_analyses": total,
            "ai_generated": ai_count,
            "human_written": human_count,
            "by_language": by_language,
            "by_model": by_model,
            "avg_confidence": round(avg_confidence, 2),
            "favorite_count": favorites
        }
    
    @staticmethod
    def toggle_favorite(db: Session, analysis_id: int, user_id: int) -> Optional[bool]:
        """
        Toggle favorite status of analysis
        
        Args:
            db: Database session
            analysis_id: Analysis ID
            user_id: User ID
            
        Returns:
            New favorite status or None if not found
        """
        analysis = db.query(AnalysisHistory).filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == user_id
        ).first()
        
        if not analysis:
            return None
        
        analysis.is_favorite = not analysis.is_favorite
        db.commit()
        
        return analysis.is_favorite
