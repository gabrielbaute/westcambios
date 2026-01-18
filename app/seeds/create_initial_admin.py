"""
Create initial admin account
"""
import os
import logging
from dotenv import load_dotenv

from app.enums import UserRole
from app.schemas import UserCreate
from app.services import UserService

load_dotenv()
logger = logging.getLogger("[ADMIN LOADER]")

def create_admin() -> bool:
    user_service = UserService()
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # verifying admin already exists
    if user_service.controller.get_user_by_email(admin_email):
        logger.info("Admin already exists")
        return False
    
    logger.info("Creating admin account")
    # creating admin
    user_in = UserCreate(
        email=admin_email,
        username=admin_username,
        password_hash=admin_password,
        is_active=True,
        role=UserRole.ADMIN
    )
    user_service.register_user(user_in)
    logger.info("Admin account created successfully")
    user_service.dispose()
    return True