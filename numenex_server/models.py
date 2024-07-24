from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime, Float, ForeignKey, UUID, String
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
    current_price = Column(Float)
    predicted_price = Column(Float)
    predictor_address = Column(String)
    validator_address = Column(String)
    chain = Column(String, nullable=False)
    prediction_end_date = Column(String, nullable=False)
    trading_pair = Column(String, nullable=False)
    status = Column(
        ENUM("feeded", "predicted", "validated", name="trade_status"), nullable=False
    )
