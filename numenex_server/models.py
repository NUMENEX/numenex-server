from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, Float, Integer, UUID, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
import uuid


class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    @property
    def created_on(self):
        return self.created_at.date()


class Trade(Base):
    __tablename__ = "trades"

    feeder_address = Column(String, nullable=False)
    token_name = Column(String, nullable=False)
    token_symbol = Column(String, nullable=False)
    hash = Column(String, nullable=False, unique=True)
    traded_price = Column(Float)
    predicted_price = Column(Float, comment="Price predicted by the miner")
    predictor_address = Column(String)
    validator_address = Column(String)
    chain_id = Column(Integer, nullable=False)
    prediction_end_date = Column(
        DateTime(timezone=True),
        nullable=False,
        comment="Date of prediction to be ended, Miner can no longer predict after this date for this txn",
    )
    trading_pair = Column(String, nullable=False)
    status = Column(
        ENUM("fed", "predicted", "ready", "validated", "expired", name="trade_status"),
        nullable=False,
    )
    roi = Column(Float, comment="Return on investment")
    token_price_on_prediction_day = Column(
        Float, comment="Actual price of the token on prediction date"
    )
    price_prediction_date = Column(
        DateTime, nullable=False, comment="Date of prediction to be happened"
    )
    signal = Column(
        ENUM("bullish", "bearish", name="trade_signal", create_type=True),
        comment="Signal for the trade",
    )
    token_price_on_trade_day = Column(
        Float, comment="Price of the token at the time of trading", nullable=False
    )
    token_address = Column(String, nullable=False)
    closeness_value = Column(
        Float,
        comment="Closeness value of the prediction, i.e. actual price - predicted price",
    )
    module_id = Column(
        String,
        nullable=False,
        comment="Module ID of the miner/validator in commune subnet",
    )


class Tempo(Base):
    __tablename__ = "tempo"
    current_tempo_end_date = Column(DateTime, nullable=False)
    future_tempo_end_date = Column(DateTime, nullable=False)
