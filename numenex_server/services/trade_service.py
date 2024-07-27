from ..models import Trade
from sqlalchemy.orm import Session
from .. import schema
from fastapi import HTTPException
from siwe import SiweMessage
import typing as ty
from ..constants import allowed_token_pairs
from datetime import datetime, timedelta


class TradeService:
    def find_all(
        self,
        sess: Session,
        *,
        participant_type: ty.Optional[str] = None,
        address: ty.Optional[str] = None,
    ):
        if participant_type is not None:
            if participant_type == "miner":
                return sess.query(Trade).filter(Trade.status == "feeded").all()
            elif participant_type == "validator":
                return sess.query(Trade).filter(Trade.status == "predicted").all()
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
        # if swap_txn.recipient != siwe_message.address:
        #     raise HTTPException(
        #         status_code=400, detail="Please put your own trade transaction)"
        #     )
        print(swap_txn)
        token_pair = swap_txn.token0.symbol + "/" + swap_txn.token1.symbol
        if token_pair not in allowed_token_pairs:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid token pair, Allowed token pairs are {allowed_token_pairs}",
            )
        seven_days_old_date = datetime.now() - timedelta(days=7)
        if datetime.fromtimestamp(int(swap_txn.timestamp)) < seven_days_old_date:
            raise HTTPException(
                status_code=400, detail="Trade is too old, it should be within 7 days"
            )
        token_name, token_symbol, token_amount = (
            (swap_txn.token0.name, swap_txn.token0.symbol, swap_txn.amount0)
            if float(swap_txn.amount0) > 0
            else (swap_txn.token1.name, swap_txn.token1.symbol, swap_txn.amount1)
        )
        token_price_on_trade_day = float(swap_txn.amountUSD) / float(token_amount)
        prediction_end_date = datetime.now() + timedelta(hours=12)
        price_prediction_date = datetime.now() + timedelta(days=1)
        db_trade: schema.Trade = Trade(
            traded_price=swap_txn.amountUSD,
            feeder_address=siwe_message.address,
            prediction_end_date=prediction_end_date,
            status="feeded",
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
