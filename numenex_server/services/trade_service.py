from ..models import Trade
from sqlalchemy.orm import Session


class TradeService:
    def find_all(self, sess: Session):
        return sess.query(Trade).all()
