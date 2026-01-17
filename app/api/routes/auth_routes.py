from fastapi import APIRouter, HTTPException, status
from app.schemas import UserLogin, Token
from app.services.user_service import UserService
from app.services.security_service import SecurityService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_for_access_token(login_data: UserLogin):
    """
    Authenticate user and return a JWT token.
    """
    user_service = UserService()
    try:
        user = user_service.authenticate_user(login_data)
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