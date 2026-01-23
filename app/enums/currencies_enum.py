from typing import List
from enum import StrEnum

class CurrencyEnum(StrEnum):
    VES = "VES"
    BRL = "BRL"
    USD = "USD"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.value
    
    def to_list(self) -> List[str]:
        return [self.value for self in CurrencyEnum]