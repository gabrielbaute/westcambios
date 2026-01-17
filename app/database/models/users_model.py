from sqlalchemy import Column, Integer, DateTime, Enum, String, Boolean

from app.database.db_base import Base
from app.enums import UserRole

class UsersDatabaseModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password_hash": self.password_hash,
            "is_active": self.is_active,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }