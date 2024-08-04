import typing as ty

from fastapi import APIRouter, Depends, Request
from ..dependencies import (
    get_session,
    get_numx_participant,
)
from .. import schema
from ..services import AnswerService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/", response_model=ty.List[schema.Answer])
async def get_answers(
    service: ty.Annotated[AnswerService, Depends(AnswerService)],
    session: Session = Depends(get_session),
):
    return service.get_answers(session)


@router.post("/", response_model=ty.Dict[str, ty.List[str]])
async def create_answers(
    service: ty.Annotated[AnswerService, Depends(AnswerService)],
    answers: ty.List[schema.AnswerCreate],
    session: Session = Depends(get_session),
    answerer: schema.SubnetUser = Depends(get_numx_participant),
):
    return service.create_answers(session, answers=answers, answerer_id=answerer.id)
