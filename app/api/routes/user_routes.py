"""
Module for defining API routes related to user management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.dependencies import get_current_user
from app.services.user_service import UserService
from app.schemas import UserResponse, UserUpdate, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)] # Protección global del router
)

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Retrieve the current user's information.
    """
    return current_user

@router.patch("/update_user", response_model=UserResponse)
def update_user(user_in: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    """
    Update the current user's information.
    """
    service = UserService()
    try:
        return service.update_user_data(current_user.id, user_in)
    finally:
        service.controller.close_session()

@router.patch("/update_password", response_model=UserResponse)
def update_password(
    new_password: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Update the current user's password.
    """
    service = UserService()
    try:
        return service.update_user_password_hash(current_user.id, new_password)
    finally:
        service.controller.close_session()

@router.patch("/update_email", response_model=UserResponse)
def update_email(
    new_email: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Update the current user's email.
    """
    service = UserService()
    try:
        return service.update_user_email(current_user.id, new_email)
    finally:
        service.controller.close_session()