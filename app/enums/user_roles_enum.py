from typing import List
from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"
    CLIENT = "CLIENT"

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return self.value
    
    def to_list(self) -> List[str]:
        return [self.value for self in UserRole]