from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

from app.enums import UserRole

class UserResponse(BaseModel):
    """
    Schema for reading user information.

    Attributes:
        id: Unique identifier of the user.
        email: Email address of the user.
        username: Username of the user.
        is_active: Flag indicating if the user is active.
        rol: Role of the user.
        created_at: Timestamp of the user creation.
        updated_at: Timestamp of the user update.
    """
    id: int
    email: EmailStr
    username: str
    is_active: bool
    rol: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "user",
                    "is_active": True,
                    "rol": "CLIENT",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-10T12:00:00Z"
                }
            ]
        }
    )

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    
    Attributes:
        email: Email address of the user.
        username: Username of the user.
        password_hash: Hashed password of the user.
        is_active: Flag indicating if the user is active.
        rol: Role of the user.
        created_at: Timestamp of the user creation.
        updated_at: Timestamp of the user update.
    """
    email: EmailStr
    username: str
    password_hash: str
    is_active: Optional[bool] = True
    rol: UserRole = UserRole.CLIENT
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "user@example.com",
                    "username": "user",
                    "password_hash": "password_hash",
                    "is_active": True,
                    "rol": "CLIENT",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-10T12:00:00Z"
                }
            ]
        }
    )

class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    rol: Optional[UserRole] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "user@example.com",
                    "username": "new_user",
                    "password": "new_password",
                    "is_active": True,
                    "rol": "ADMIN",
                    "updated_at": "2023-10-10T12:00:00Z"
                }
            ]
        }
    )

class UserLogin(BaseModel):
    """
    Schema for user login.
    
    Atributes:
        email: Email address of the user.
        password_hash: Password of the user.
    """
    email: EmailStr
    password_hash: str