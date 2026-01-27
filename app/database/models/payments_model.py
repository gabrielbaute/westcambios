from __future__ import annotations # Permite usar tipos que aún no están definidos
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, DateTime, Enum, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db_base import Base
from app.enums import PaymentStatus, CurrencyEnum

# Evita la importación circular en tiempo de ejecución, pero permite el tipado en el IDE
if TYPE_CHECKING:
    from app.database.models.users_model import UsersDatabaseModel

class PaymentsDatabaseModel(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    operation_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False)

    # Relationships
    # Nota: Usamos strings para las referencias de clase para evitar dependencias rígidas
    user: Mapped["UsersDatabaseModel"] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return (f"<Payment(id_user={self.id_user}, amount={self.amount}, "
                f"currency={self.currency}, status={self.status})>")
    
    def __str__(self) -> str:
        return f"{self.id_user}: {self.amount} {self.currency} ({self.status})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_user": self.id_user,
            "amount": self.amount,
            "currency": self.currency.value if hasattr(self.currency, 'value') else self.currency,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "operation_id": self.operation_id,
            "status": self.status.value if hasattr(self.status, 'value') else self.status
        }