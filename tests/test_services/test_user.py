from app.schemas import UserCreate
from app.enums import UserRole

def test_register_user_duplicate_email(user_service):
    """Ensures that the service prevents duplicate email registration."""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password_hash="plain_password", # El servicio le hará el hash
        role=UserRole.CLIENT
    )
    
    # Primer registro: Exitoso
    first_user = user_service.register_user(user_data)
    assert first_user is not None
    
    # Segundo registro: Debe fallar por validación de email
    duplicate_user = user_service.register_user(user_data)
    assert duplicate_user is None