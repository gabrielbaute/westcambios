from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from app.enums import CurrencyEnum

class RateResponse(BaseModel):
    """
    Rate response model.

    Attributes:
        id: Unique identifier of the rate.
        from_currency: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        timestamp: Timestamp of the rate creation.
    """
    id: int
    from_currency: CurrencyEnum
    to_currency: CurrencyEnum
    rate: float
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "from_currency": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90,
                    "timestamp": "2023-10-01T12:00:00Z"
                }
            ]
        }
    )

class RateListResponse(BaseModel):
    """
    Rate list response model.

    Attributes:
        count: Total number of rates.
        rates: List of rate responses.
    """
    count: int
    rates: List[Optional[RateResponse]] = []

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "count": 2,
                    "rates": [
                        {
                            "id": 1,
                            "from_curreny": "BRL",
                            "to_currency": "VES",
                            "rate": 95.90,
                            "timestamp": "2023-10-01T12:00:00Z"
                        },
                        {
                            "id": 2,
                            "from_curreny": "USD",
                            "to_currency": "VES",
                            "rate": 94.90,
                            "timestamp": "2023-10-02T12:00:00Z"
                        }
                    ]
                }
            ]
        }
    )


class RateCreate(BaseModel):
    """
    Rate creation model.
    
    Attributes:
        from_currency: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        timestamp: Timestamp of the rate creation.
    """
    from_currency: CurrencyEnum
    to_currency: CurrencyEnum
    rate: float
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "from_currency": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90,
                    "timestamp": "2023-10-01T12:00:00Z"
                }
            ]
        }
    )

class RateUpdate(BaseModel):
    """
    Rate update model.

    Attributes:
        from_currency: Currency code of the source currency.
        to_currency: Currency code of the target currency.
        rate: Exchange rate value.
        timestamp: Timestamp of the rate creation.
    """
    from_currency: Optional[CurrencyEnum] = None
    to_currency: Optional[CurrencyEnum] = None
    rate: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "from_currency": "BRL",
                    "to_currency": "VES",
                    "rate": 95.90
                }
            ]
        }
    )