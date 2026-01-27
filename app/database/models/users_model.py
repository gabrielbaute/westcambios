from datetime import datetime
from typing import List, Optional
from sqlalchemy import Integer, DateTime, Enum, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import UserRole
from app.database.db_base import Base
from app.database.models.payments_model import PaymentsDatabaseModel


class UsersDatabaseModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    payments: Mapped[List["PaymentsDatabaseModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan" # Opcional: si borras usuario, borra sus pagos
    )

    def __repr__(self) -> str:
        return f"<User(username={self.username}, role={self.role})>"