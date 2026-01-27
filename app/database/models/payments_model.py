from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database.db_base import Base
from app.enums import PaymentStatus, CurrencyEnum

class PaymentsDatabaseModel(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    operation_id = Column(String, nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False)

    # Backrefs
    user = relationship("UsersDatabaseModel", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id_user={self.id_user}, amount={self.amount}, currency={self.currency}, payment_date={self.payment_date}, status={self.status})>"
    
    def __str__(self):
        return f"{self.id_user}: {self.amount} {self.currency} ({self.status})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "amount": self.amount,
            "currency": self.currency,
            "payment_date": self.payment_date,
            "operation_id": self.operation_id,
            "status": self.status
        }