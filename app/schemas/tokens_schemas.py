from typing import Optional
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    """
    Schema for JWT token.

    Attributes:
        access_token: JWT access token.
        token_type: Type of the token.
    """
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            ]
        }
    )


class TokenData(BaseModel):
    """
    Schema for JWT token data.

    Attributes:
        username: Username associated with the token.
    """
    username: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "user@example.com"
                }
            ]
        }
    )