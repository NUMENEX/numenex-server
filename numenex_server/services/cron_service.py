from ..models import Trade
from sqlalchemy.orm import Session
from sqlalchemy import update
from datetime import datetime
import typing as ty


class CronService:
    def update_trades(self, session: Session) -> None:
        trades = session.query(Trade).filter(Trade.status == "predicted" or "fed").all()
        trade_updates: ty.List[Trade] = []
        for trade in trades:
            if trade.status == "fed" and trade.prediction_end_date < datetime.now():
                trade.status = "expired"
                trade_updates.append(trade)
            elif (
                trade.status == "predicted"
                and trade.price_prediction_date < datetime.now()
            ):
                # fetch price from api and update the price
                trade.token_price_on_prediction_day = 100
                trade.status = "ready"
                trade.roi = (
                    (
                        (
                            trade.token_price_on_prediction_day
                            - trade.token_price_on_trade_day
                        )
                        * 100
                        / trade.token_price_on_trade_day
                    )
                    if trade.token_price_on_trade_day
                    else 0
                )
                trade.closeness_value = (
                    trade.token_price_on_prediction_day - trade.predicted_price
                )

                trade_updates.append(trade)

        session.execute(update[Trade], trade_updates)
