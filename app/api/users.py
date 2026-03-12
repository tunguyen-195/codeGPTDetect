"""User management API endpoints"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate, UserList
from app.schemas.response import SuccessResponse, MessageResponse
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    """
    updated_user = UserService.update_user(db, current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.delete("/me", response_model=MessageResponse)
async def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete current user's account
    """
    success = UserService.delete_user(db, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return MessageResponse(
        message="Account deleted successfully"
    )


# Admin endpoints
@router.get("", response_model=UserList, dependencies=[Depends(require_role("admin"))])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all users (Admin only)
    
    - **skip**: Pagination offset
    - **limit**: Number of users per page
    - **role**: Filter by role
    - **is_active**: Filter by active status
    """
    users = UserService.get_users(db, skip, limit, role, is_active)
    total = UserService.count_users(db, role, is_active)
    
    return UserList(
        users=users,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user by ID (Admin only)
    """
    user = UserService.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user (Admin only)
    """
    updated_user = UserService.update_user(db, user_id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.delete("/{user_id}", response_model=MessageResponse, dependencies=[Depends(require_role("admin"))])
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete user (Admin only)
    """
    success = UserService.delete_user(db, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return MessageResponse(
        message="User deleted successfully"
    )


@router.patch("/{user_id}/role", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def update_user_role(
    user_id: int,
    new_role: str = Query(..., pattern="^(admin|user|viewer)$"),
    db: Session = Depends(get_db)
):
    """
    Update user role (Admin only)
    
    - **new_role**: admin, user, or viewer
    """
    updated_user = UserService.update_role(db, user_id, new_role)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.patch("/{user_id}/status", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Toggle user active status (Admin only)
    """
    updated_user = UserService.toggle_active_status(db, user_id)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user
