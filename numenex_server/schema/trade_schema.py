from pydantic import BaseModel
from typing import Optional

__all__ = ["Trade", "TradeCreate"]


class TradeBase(BaseModel):
    feeder_address: str
    token_name: str
    token_symbol: str
    hash: str
    current_price: float
    predicted_price: Optional[float]
    predictor_address: Optional[str]
    validator_address: Optional[str]
    chain: str
    prediction_end_date: str
    trading_pair: str
    status: str


class Trade(TradeBase):
    class Config:
        from_attributes = True


class TradeCreate(TradeBase): ...
