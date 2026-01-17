"""
Unit tests for SecurityService.
"""
from app.services.security_service import SecurityService
from app.services.user_service import UserService
from app.schemas import UserCreate, UserLogin
from app.enums import UserRole

def test_password_hashing():
    """
    Formal test for the hashing property
    """
    password = "secret_password_123"
    hashed = SecurityService.get_password_hash(password)
    
    assert hashed != password
    assert SecurityService.verify_password(password, hashed) is True
    assert SecurityService.verify_password("wrong_password", hashed) is False

def test_jwt_generation_and_decoding():
    """Test token lifecycle: Creation -> Decoding -> Data Integrity."""
    data = {"sub": "gabriel@example.com"}
    token = SecurityService.create_access_token(data)
    
    decoded_data = SecurityService.decode_access_token(token)
    
    assert decoded_data.username == data["sub"]


def test_full_auth_flow():
    user_service = UserService()
    email = "test_auth@example.com"
    password = "secure_password"
    
    # 1. Registro
    user_in = UserCreate(
        email=email,
        username="auth_tester",
        password_hash=password, # Se enviará como '1234' y el servicio lo hasheará
        role=UserRole.CLIENT
    )
    user_service.register_user(user_in)
    
    # 2. Autenticación (Login)
    login_data = UserLogin(email=email, password=password)
    authenticated_user = user_service.authenticate_user(login_data)
    
    assert authenticated_user is not None
    assert authenticated_user.email == email
    
    # 3. Generación de Token
    token = SecurityService.create_access_token(data={"sub": authenticated_user.email})
    assert token is not None
    
    # 4. Verificación de integridad del Token
    decoded = SecurityService.decode_access_token(token)
    assert decoded.username == email