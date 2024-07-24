import typing as ty

from fastapi import APIRouter, Depends
from ..dependencies import get_session, get_miner, get_validator
from .. import schema
from ..services import TradeService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/", response_model=ty.List[schema.Trade])
async def get_trades(
    service: ty.Annotated[TradeService, Depends(TradeService)],
    session: Session = Depends(get_session),
    # _: ty.Any = Depends(get_miner),
):
    data = service.find_all(session)
    return data


@router.post("/", response_model=schema.Trade)
async def create_trade(
    trade: schema.TradeCreate,
    service: ty.Annotated[TradeService, Depends(TradeService)],
    session: Session = Depends(get_session),
    # _: ty.Any = Depends(get_miner),
):
    return service.create_trade(trade, session)


@router.put("/miner/{trade_id}", response_model=schema.Trade)
async def update_trade_miner(
    trade_id: str,
    trade: schema.TradeUpdateMiner,
    service: ty.Annotated[TradeService, Depends(TradeService)],
    session: Session = Depends(get_session),
    miner_address: str = Depends(get_miner),
):
    return service.update_trade(
        session, trade_id=trade_id, trade=trade, address=miner_address, type="miner"
    )


@router.put("/validator/{trade_id}", response_model=schema.Trade)
async def update_trade_validator(
    trade_id: str,
    trade: schema.TradeUpdateValidator,
    service: ty.Annotated[TradeService, Depends(TradeService)],
    session: Session = Depends(get_session),
    vali_address: str = Depends(get_validator),
):
    return service.update_trade(
        sess=session,
        trade_id=trade_id,
        trade=trade,
        address=vali_address,
        type="validator",
    )
