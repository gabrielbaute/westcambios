"""
Seed for test users logic
"""
from app.enums import UserRole
from app.schemas import UserCreate
from app.services import UserService

def create_users():
    user_service = UserService()
    user_admin = UserCreate(
        email="admin@example.com",
        username="admin",
        password_hash="1234",
        is_active=True,
        role=UserRole.ADMIN
    )
    user_client = UserCreate(
        email="user@example.com",
        username="user",
        password_hash="1234",
        is_active=True,
        role=UserRole.CLIENT
    )
    user_service.register_user(user_admin)
    user_service.register_user(user_client)
    user_service.dispose()

if __name__ == "__main__":
    create_users()