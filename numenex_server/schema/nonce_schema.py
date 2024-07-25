from pydantic import BaseModel

__all__ = ["Nonce", "NonceBase"]


class NonceBase(BaseModel):
    nonce: str


class Nonce(NonceBase):
    class Config:
        from_attributes = True
