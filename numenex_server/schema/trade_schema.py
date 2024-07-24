from pydantic import BaseModel
from typing import Optional
from datetime import datetime

__all__ = ["Trade", "TradeCreate", "TradeUpdateMiner", "TradeUpdateValidator"]


class TradeBase(BaseModel):
    token_name: str
    token_symbol: str
    hash: str
    chain: str
    trading_pair: str


class Trade(TradeBase):
    feeder_address: str
    current_price: float
    predicted_price: Optional[float]
    predictor_address: Optional[str]
    validator_address: Optional[str]
    prediction_end_date: datetime
    price_prediction_date: datetime
    status: str
    roi: Optional[float]
    actual_price: Optional[float]

    class Config:
        from_attributes = True


class TradeCreate(TradeBase): ...


class TradeUpdateMiner(BaseModel):
    predicted_price: float


class TradeUpdateValidator(BaseModel):
    predicted_price: float
    actual_price: float
    roi: float
