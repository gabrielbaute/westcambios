from typing import List
from enum import StrEnum

class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CANCELED = "CANCELED"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.value
    
    def to_list(self) -> List[str]:
        return [self.value for self in PaymentStatus]