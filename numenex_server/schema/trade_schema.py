from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import typing as ty
import uuid

__all__ = [
    "Trade",
    "TradeUpdateMiner",
    "TradeUpdateValidator",
    "SwapResponse",
]


class Trade(BaseModel):
    id: uuid.UUID
    feeder_address: str
    token_price_on_trade_day: float
    predicted_price: Optional[float]
    predictor_address: Optional[str]
    validator_address: Optional[str]
    prediction_end_date: datetime
    price_prediction_date: datetime
    status: str
    roi: Optional[float]
    token_price_on_prediction_day: Optional[float]
    hash: str
    token_name: str
    token_symbol: str
    trading_pair: str
    signal: Optional[str]
    token_address: str
    closeness_value: Optional[float]
    module_id: Optional[str]

    class Config:
        from_attributes = True


class TradeUpdateMiner(BaseModel):
    predicted_price: float
    signal: ty.Literal["bearish", "bullish"]


class TradeUpdateValidator(BaseModel):
    predicted_price: float
    actual_price: float
    roi: float


class TokenData(BaseModel):
    id: str
    name: str
    symbol: str


class SwapResponse(BaseModel):
    amount0: str
    amount1: str
    amountUSD: str
    id: str
    logIndex: str
    origin: str
    recipient: str
    sender: str
    sqrtPriceX96: str
    tick: str
    timestamp: str
    token0: TokenData
    token1: TokenData
