import typing as ty

from fastapi import APIRouter, Depends, Request
from ..dependencies import (
    get_session,
    get_validator,
    verify_trade,
    get_numx_participant,
    get_siwe_msg,
)
from .. import schema
from ..services import QuestionService
from sqlalchemy.orm import Session


router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=ty.List[schema.Question])
async def get_questions(
    service: ty.Annotated[QuestionService, Depends(QuestionService)],
    session: Session = Depends(get_session),
):
    return service.get_questions(session)


@router.post("/", response_model=ty.List[schema.Question])
async def create_questions(
    service: ty.Annotated[QuestionService, Depends(QuestionService)],
    questions: ty.List[schema.QuestionCreate],
    session: Session = Depends(get_session),
):
    return service.create_questions(session, questions=questions)
