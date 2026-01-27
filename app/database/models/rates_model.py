from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db_base import Base
from app.enums import CurrencyEnum

class RatesDatabaseModel(Base):
    __tablename__ = 'rates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)
    to_currency: Mapped[CurrencyEnum] = mapped_column(Enum(CurrencyEnum), nullable=False)
    rate: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Rate(from_currency={self.from_currency}, to_currency={self.to_currency}, rate={self.rate}, timestamp={self.timestamp})>"
    
    def __str__(self):
        return f"{self.from_currency} to {self.to_currency}: {self.rate}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "rate": self.rate,
            "timestamp": self.timestamp
        }