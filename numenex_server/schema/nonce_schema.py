from pydantic import BaseModel
from typing import Optional

__all__ = ["Nonce", "NonceBase", "Session"]


class NonceBase(BaseModel):
    nonce: str


class Nonce(NonceBase):
    class Config:
        from_attributes = True


class Session(BaseModel):
    address: Optional[str]
    chainId: Optional[str]

    class Config:
        from_attributes = True
