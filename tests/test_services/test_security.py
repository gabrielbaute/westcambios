"""
Unit tests for SecurityService.
"""
from app.services.security_service import SecurityService

def test_password_hashing():
    """
    Formal test for the hashing property:
    $\forall p \in \text{Passwords}, \text{verify}(p, \text{hash}(p)) = \text{True}$
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