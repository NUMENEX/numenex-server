from pydantic import BaseModel
import typing as ty
import uuid
from .base_schema import DatabaseMixin
from .subnet_user_schema import SubnetUser

__all__ = ["AnswerBase", "AnswerCreate", "Answer", "AnswerUpdate"]


class AnswerBase(BaseModel):
    answer: str
    question_id: uuid.UUID
    supporting_resources: ty.Optional[ty.Dict[str, ty.Any]]


class AnswerCreate(AnswerBase): ...


class Answer(AnswerBase, DatabaseMixin):
    miner: SubnetUser

    class Config:
        from_attributes = True


class AnswerUpdate(BaseModel):
    id: uuid.UUID
    score: float
