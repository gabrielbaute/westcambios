from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.services.security_service import SecurityService
from app.services.user_service import UserService
from app.schemas import UserResponse
from app.enums import UserRole

# Esto permite que Swagger UI muestre el botón de "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Dependency to validate the JWT token and return the current user.
    """
    # 1. Decodificar el token
    token_data = SecurityService.decode_access_token(token)
    
    # 2. Buscar al usuario en la DB (usando el email que viene en 'sub')
    user_service = UserService()
    try:
        user = user_service.controller.get_user_by_email(token_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )
        return user
    finally:
        user_service.controller.close_session()

def get_current_admin(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Dependency to ensure the current user has the ADMIN role.
    """
    user_role_map: dict[str, UserRole] = {
        "ADMIN": UserRole.ADMIN,
        "CLIENT": UserRole.CLIENT
        }
    role = user_role_map.get(current_user.role)
    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user