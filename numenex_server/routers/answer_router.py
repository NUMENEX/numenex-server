import typing as ty

from fastapi import APIRouter, Depends, HTTPException, status
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
    if answerer.user_type != "miner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only miners are allowed to answer questions",
        )
    return service.create_answers(session, answers=answers, answerer_id=answerer.id)


@router.patch("/", response_model=ty.Dict[str, ty.List[ty.Dict[str, ty.Any]]])
async def update_answer_validations(
    service: ty.Annotated[AnswerService, Depends(AnswerService)],
    validations: ty.List[schema.AnswerUpdate],
    session: Session = Depends(get_session),
    validator: schema.SubnetUser = Depends(get_numx_participant),
):
    if validator.user_type != "validator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only validators are allowed to update answer validations",
        )
    updated_answers = service.update_answer_validations(
        session,
        validations=validations,
        ss58_address=validator.user_address,
        module_id=validator.module_id,
    )
    return {"updated_answers": updated_answers}
