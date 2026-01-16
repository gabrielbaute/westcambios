from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.enums import CurrencyEnum

class RateResponse(BaseModel):
    """
    Rate response model.

    Attributes:
        id: Unique identifier of the rate.
        from_curreny: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        created_at: Timestamp of the rate creation.
    """
    id: int
    from_curreny: CurrencyEnum
    to_currency: CurrencyEnum
    rate: float
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "from_curreny": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90,
                    "created_at": "2023-10-01T12:00:00Z"
                }
            ]
        }
    )

class RateCreate(BaseModel):
    """
    Rate creation model.
    
    Attributes:
        from_curreny: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        created_at: Timestamp of the rate creation.
    """
    from_curreny: CurrencyEnum
    to_currency: CurrencyEnum
    rate: float
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "from_curreny": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90,
                    "created_at": "2023-10-01T12:00:00Z"
                }
            ]
        }
    )

class RateUpdate(BaseModel):
    """
    Rate update model.

    Attributes:
        from_curreny: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        created_at: Timestamp of the rate creation.
    """
    from_curreny: Optional[CurrencyEnum] = None
    to_currency: Optional[CurrencyEnum] = None
    rate: Optional[float] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "from_curreny": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90,
                    "created_at": "2023-10-01T12:00:00Z"
                }
            ]
        }
    )