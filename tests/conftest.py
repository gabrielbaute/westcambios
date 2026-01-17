"""
Pytest configuration and global fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db_base import Base
from app.services import UserService

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def user_service(db_session):
    """Fixture to provide a UserService with a clean session."""
    service = UserService()
    # Inyectamos la sesión de prueba en el controlador del servicio
    service.controller.session = db_session
    return service