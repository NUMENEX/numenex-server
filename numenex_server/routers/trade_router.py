import typing as ty

from fastapi import APIRouter, Depends
from ..dependencies import get_session
from .. import schema
from ..services import TradeService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/", response_model=ty.List[schema.Trade])
async def get_trades(
    service: ty.Annotated[TradeService, Depends(TradeService)],
    session: Session = Depends(get_session),
):
    data = service.find_all(session)
    return data
