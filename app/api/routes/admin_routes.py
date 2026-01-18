"""
Module for defining API routes related to admin management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.enums import UserRole
from app.api.dependencies import get_current_admin
from app.services.user_service import UserService
from app.services.rates_service import RateService
from app.schemas import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    RateCreate, RateUpdate, RateResponse
)

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
    dependencies=[Depends(get_current_admin)] # Protección global del router
)

# --- GESTIÓN DE USUARIOS ---

@router.post("/register_user", response_model=UserResponse)
def create_user(user_in: UserCreate):
    service = UserService()
    try:
        user = service.register_user(user_in)
        if not user:
            raise HTTPException(status_code=400, detail="User could not be created")
        return user
    finally:
        service.controller.close_session()

@router.patch("/update_user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate):
    service = UserService()
    try:
        return service.update_user_data(user_id, user_in)
    finally:
        service.controller.close_session()

@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    service = UserService()
    try:
        if not service.delete_user(user_id):
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        service.controller.close_session()

@router.patch("/activate_user/{user_id}", response_model=UserResponse)
def activate_user(user_id: int):
    service = UserService()
    try:
        return service.activate_user(user_id)
    finally:
        service.controller.close_session()

@router.patch("/deactivate_user/{user_id}", response_model=UserResponse)
def deactivate_user(user_id: int):
    service = UserService()
    try:
        return service.deactivate_user(user_id)
    finally:
        service.controller.close_session()

@router.patch("/update_user_role/{user_id}", response_model=UserResponse)
def update_user_role(user_id: int, user_role: str):
    service = UserService()
    user_role_map: dict[str, UserRole] = {
        "ADMIN": UserRole.ADMIN,
        "CLIENT": UserRole.CLIENT
    }
    try:
        return service.update_user_role(user_id, user_role = user_role_map.get(user_role))
    finally:
        service.controller.close_session()

# --- VISUALIZAR USUARIOS POR PERÍODOS ---

@router.get("/users_register_last_month", response_model=UserListResponse)
def get_users_register_last_month():
    service = UserService()
    try:
        return service.get_user_register_last_month()
    finally:
        service.controller.close_session()

@router.get("/users_register_last_3_months", response_model=UserListResponse)
def get_users_register_last_3_months():
    service = UserService()
    try:
        return service.get_user_register_last_3_months()
    finally:
        service.controller.close_session()

@router.get("/users_register_last_6_months", response_model=UserListResponse)
def get_users_register_last_6_months():
    service = UserService()
    try:
        return service.get_user_register_last_6_months()
    finally:
        service.controller.close_session()

@router.get("/users_register_last_year", response_model=UserListResponse)
def get_users_register_last_year():
    service = UserService()
    try:
        return service.get_user_register_last_year()
    finally:
        service.controller.close_session()

@router.get("/users_by_custom_range", response_model=UserListResponse)
def get_users_by_custom_range(start_date: str, end_date: str):
    service = UserService()
    try:
        return service.get_users_by_custom_range(start_date, end_date)
    finally:
        service.controller.close_session()

# --- GESTIÓN DE TASAS (RATES) ---

@router.post("/register_rate", response_model=RateResponse)
def register_rate(rate_in: RateCreate):
    service = RateService()
    try:
        return service.register_rate(rate_in)
    finally:
        service.controller.close_session()

@router.patch("/update_rate/{rate_id}", response_model=RateResponse)
def update_rate(rate_id: int, rate_in: RateUpdate):
    service = RateService()
    try:
        return service.update_rate(rate_id, rate_in)
    finally:
        service.controller.close_session()

@router.delete("/delete_rate/{rate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rate(rate_id: int):
    service = RateService()
    try:
        if not service.delete_rate(rate_id):
            raise HTTPException(status_code=404, detail="Rate record not found")
    finally:
        service.controller.close_session()