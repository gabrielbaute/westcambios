"""
Seed for test users logic
"""
from app.enums import UserRole
from app.schemas import UserCreate
from app.services import UserService

def create_users():
    user_service = UserService()
    user_in = UserCreate(
        email="admin@example.com",
        username="admin",
        password_hash="1234",
        is_active=True,
        role=UserRole.ADMIN
    )
    user_in = UserCreate(
        email="user@example.com",
        username="user",
        password_hash="1234",
        is_active=True,
        role=UserRole.CLIENT
    )
    user_service.register_user(user_in)
    user_service.register_user(user_in)