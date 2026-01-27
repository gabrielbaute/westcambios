from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.enums import CurrencyEnum, PaymentStatus

class PaymentResponse(BaseModel):
    """
    Payment response model

    Arguements:
        id(int): Unique identifier of the payment
        id_user(int): Unique identifier of the user
        amount(float): Amount of the payment
        currency(CurrencyEnum): Currency of the payment
        payment_date(datetime): Date and time of the payment
        operation_id(Optional[str]): Operation ID of the payment
        status(PaymentStatus): Status of the payment
    """
    id: int
    id_user: int
    amount: float
    currency: CurrencyEnum
    payment_date: datetime
    operation_id: Optional[str] = None
    status: PaymentStatus

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "id_user": 1,
                    "amount": 100.00,
                    "currency": "BRL",
                    "payment_date": "2023-10-01T12:00:00Z",
                    "operation_id": "1234567890",
                    "status": "PENDING"
                }
            ]
        }
    )

class PaymentListResponse(BaseModel):
    """
    Payment list response model

    Arguements:
        count(int): Total number of payments
        payments(List[Optional[PaymentResponse]]): List of payment responses
    """
    count: int
    payments: List[Optional[PaymentResponse]] = []

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "count": 2,
                    "payments": [
                        {
                            "id": 1,
                            "id_user": 1,
                            "amount": 100.00,
                            "currency": "BRL",
                            "payment_date": "2023-10-01T12:00:00Z",
                            "operation_id": "1234567890",
                            "status": "PENDING"
                        },
                        {
                            "id": 2,
                            "id_user": 1,
                            "amount": 120.00,
                            "currency": "BRL",
                            "payment_date": "2023-10-02T12:00:00Z",
                            "operation_id": "0987654321",
                            "status": "COMPLETED"
                        }
                    ]
                }
            ]
        }
    )

class PaymentCreate(BaseModel):
    """
    Payment creation model

    Arguements:
        id_user(int): Unique identifier of the user
        amount(float): Amount of the payment
        currency(CurrencyEnum): Currency of the payment
        payment_date(datetime): Date and time of the payment
        operation_id(Optional[str]): Operation ID of the payment
        status(PaymentStatus): Status of the payment
    """
    id_user: int
    amount: float
    currency: CurrencyEnum
    payment_date: Optional[datetime] = None
    operation_id: Optional[str] = None
    status: Optional[PaymentStatus] = PaymentStatus.PENDING

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id_user": 1,
                    "amount": 100.00,
                    "currency": "BRL",
                    "payment_date": "2023-10-01T12:00:00Z",
                    "operation_id": "1234567890",
                    "status": "PENDING"
                }
            ]
        }
    
    )

class PaymentUpdate(BaseModel):
    """
    Payment update model

    Arguements:
        id_user(Optional[int]): Unique identifier of the user
        amount(Optional[float]): Amount of the payment
        currency(Optional[CurrencyEnum]): Currency of the payment
        payment_date(Optional[datetime]): Date and time of the payment
        operation_id(Optional[str]): Operation ID of the payment
        status(Optional[PaymentStatus]): Status of the payment
    """
    id_user: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[CurrencyEnum] = None
    payment_date: Optional[datetime] = None
    operation_id: Optional[str] = None
    status: Optional[PaymentStatus] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id_user": 1,
                    "amount": 100.00,
                    "currency": "BRL",
                    "payment_date": "2023-10-01T12:00:00Z",
                    "operation_id": "1234567890",
                    "status": "PENDING"
                }
            ]
        }
    )