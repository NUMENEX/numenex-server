from ..models import Trade, Tempo
from sqlalchemy.orm import Session
from .. import schema
from fastapi import HTTPException
from siwe import SiweMessage
import typing as ty
from ..constants import allowed_tokens
from datetime import datetime, timedelta
from sqlalchemy import or_


class TradeService:
    def find_all(
        self,
        sess: Session,
        *,
        participant_type: ty.Optional[str] = None,
        address: ty.Optional[str] = None,
    ):
        tempo_data = sess.query(Tempo).all()
        if len(tempo_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="Tempo data not found, please ask your owner to update it",
            )
        tempo = tempo_data[0]
        if participant_type is not None:
            if participant_type == "miner":
                return sess.query(Trade).filter(Trade.status == "fed").all()
            elif participant_type == "validator":
                return (
                    sess.query(Trade)
                    .filter(
                        or_(Trade.status == "ready", Trade.status == "validated"),
                        Trade.price_prediction_date == tempo.current_tempo_end_date,
                    )
                    .all()
                )
        else:
            return sess.query(Trade.feeder_address == address).all()

    def create_trade(
        self,
        sess: Session,
        *,
        siwe_message: SiweMessage,
        message: ty.Dict[str, any],
        swap_array: ty.List[schema.SwapResponse],
    ):
        swap_txn = schema.SwapResponse(**swap_array[0])
        # TODO:: Uncomment this after testing
        if swap_txn.recipient != siwe_message.address:
            raise HTTPException(
                status_code=400, detail="Please put your own trade transaction)"
            )
        token_pair = swap_txn.token0.symbol + "/" + swap_txn.token1.symbol
        token_id, token_name, token_symbol, token_amount = (
            (
                swap_txn.token0.id,
                swap_txn.token0.name,
                swap_txn.token0.symbol,
                swap_txn.amount0,
            )
            if float(swap_txn.amount0) > 0
            else (
                swap_txn.token1.id,
                swap_txn.token1.name,
                swap_txn.token1.symbol,
                swap_txn.amount1,
            )
        )
        normalized_token_addresses = [
            self.normalize_address(token) for token in allowed_tokens.values()
        ]
        if self.normalize_address(token_id) not in normalized_token_addresses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid token, Allowed tokens are {allowed_tokens}",
            )
        seven_days_old_date = datetime.now() - timedelta(days=7)
        if datetime.fromtimestamp(int(swap_txn.timestamp)) < seven_days_old_date:
            raise HTTPException(
                status_code=400, detail="Trade is too old, it should be within 7 days"
            )

        # TODO:: do a api call to fetch token price
        token_price_on_trade_day = float(swap_txn.amountUSD) / float(token_amount)
        tempo_data = sess.query(Tempo).all()
        if len(tempo_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="Tempo data not found, please ask your owner to update it",
            )
        tempo = tempo_data[0]
        prediction_end_date = tempo.current_tempo_end_date - timedelta(hours=12)
        price_prediction_date = tempo.current_tempo_end_date
        if prediction_end_date < datetime.now():
            prediction_end_date = tempo.future_tempo_end_date - timedelta(hours=12)
            price_prediction_date = tempo.future_tempo_end_date
        prediction_end_date = datetime.now() + timedelta(hours=12)
        price_prediction_date = datetime.now() + timedelta(days=1)
        db_trade: schema.Trade = Trade(
            traded_price=swap_txn.amountUSD,
            feeder_address=siwe_message.address,
            prediction_end_date=prediction_end_date,
            status="fed",
            price_prediction_date=price_prediction_date,
            chain_id=42161,
            hash=message["hash"],
            trading_pair=token_pair,
            token_name=token_name,
            token_symbol=token_symbol,
            token_price_on_trade_day=token_price_on_trade_day,
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
        module_id: str,
    ):
        db_trade = sess.query(Trade).filter(Trade.id == trade_id).first()
        if not db_trade:
            raise HTTPException(status_code=404, detail="Trade not found")
        if db_trade.status == "validated" or db_trade.status == "expired":
            raise HTTPException(
                status_code=400, detail="Trade is either expired of validated"
            )
        now = datetime.now()
        for key, value in trade:
            setattr(db_trade, key, value)
        if type == "miner":
            if db_trade.status != "fed":
                raise HTTPException(status_code=400, detail="Trade already predicted")
            if now > db_trade.prediction_end_date:
                raise HTTPException(
                    status_code=400, detail="You can no longer predict this transaction"
                )
            setattr(db_trade, "predictor_address", address)
            setattr(db_trade, "status", "predicted")
        elif type == "validator":
            if db_trade.status != "ready":
                raise HTTPException(
                    status_code=400, detail="Trade not yet ready for validation"
                )
            setattr(db_trade, "validator_address", address)
            setattr(db_trade, "status", "validated")
        else:
            raise HTTPException(status_code=400, detail="Invalid type")
        setattr(db_trade, "module_id", module_id)
        sess.commit()
        sess.refresh(db_trade)
        return db_trade

    def normalize_address(self, address: str):
        return address.strip().lower()
