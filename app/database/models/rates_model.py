from sqlalchemy import Column, Integer, Float, DateTime, Enum

from app.database.db_base import Base
from app.enums import CurrencyEnum

class RatesDatabaseModel(Base):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_currency = Column(Enum(CurrencyEnum), nullable=False)
    to_currency = Column(Enum(CurrencyEnum), nullable=False)
    rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

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