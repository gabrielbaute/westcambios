"""
Module for defining API routes related to user authentication.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.enums import UserRole
from app.services.user_service import UserService
from app.services.security_service import SecurityService
from app.schemas import UserLogin, Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user via Swagger Form or JSON and return a JWT token.
    """
    user_service = UserService()
    try:
        # OAuth2PasswordRequestForm usa 'username' para el campo de login
        # En tu caso, ese campo es el email.
        login_credentials = UserLogin(
            email=form_data.username, 
            password=form_data.password
        )
        
        user = user_service.authenticate_user(login_credentials)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = SecurityService.create_access_token(
            data={"sub": user.email}
        )
        
        return Token(access_token=access_token, token_type="bearer")
    finally:
        user_service.controller.close_session()
    
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_client(user_in: UserCreate):
    """
    Public endpoint to register a new client account.
    Role is strictly set to CLIENT.
    """
    user_service = UserService()
    try:
        # Forzamos seguridad: Solo CLIENT puede registrarse vía pública
        user_in.role = UserRole.CLIENT
        
        user = user_service.register_user(user_in)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        return user
    finally:
        user_service.controller.close_session()