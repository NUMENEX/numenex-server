from ..models import Trade
from sqlalchemy.orm import Session
from .. import schema
from fastapi import HTTPException
from siwe import SiweMessage
import typing as ty
import eth_hash


class TradeService:
    def find_all(self, sess: Session):
        return sess.query(Trade).all()

    def create_trade(
        self,
        sess: Session,
        *,
        trade: schema.TradeCreate,
        siwe_message: SiweMessage,
        message: ty.Dict[str, any],
    ):
        txn_details = eth_hash
        db_trade: schema.Trade = Trade(
            **trade.model_dump(),
            current_price=10,
            feeder_address=siwe_message.address,
            prediction_end_date="2021-10-10",
            status="feeded",
            price_prediction_date="2021-10-10",
            hash=message["hash"],
        )
        sess.add(db_trade)
        sess.commit()
        sess.refresh(db_trade)
        return db_trade

    def update_trade(
        self,
        sess: Session,
        *,
        trade_id: int,
        trade: schema.TradeUpdateMiner | schema.TradeUpdateValidator,
        address: str,
        type: str,
    ):
        db_trade = sess.query(Trade).filter(Trade.id == trade_id).first()

        for key, value in trade:
            setattr(db_trade, key, value)
        if type == "miner":
            setattr(db_trade, "predictor_address", address)
        elif type == "validator":
            setattr(db_trade, "validator_address", address)
        else:
            raise HTTPException(status_code=400, detail="Invalid type")
        sess.commit()
        sess.refresh(db_trade)
        return db_trade
