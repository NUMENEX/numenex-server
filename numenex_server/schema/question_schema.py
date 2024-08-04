from pydantic import BaseModel
import typing as ty
from datetime import datetime
from .base_schema import DatabaseMixin

__all__ = ["QuestionBase", "QuestionCreate", "Question"]


class QuestionBase(BaseModel):
    question: str
    question_type: ty.Literal["multiple_choice", "short_answer", "true_false"]
    answer_choices: ty.Optional[ty.Dict[str, str]]
    start_date: datetime
    end_date: datetime


class QuestionCreate(QuestionBase): ...


class Question(QuestionBase, DatabaseMixin):
    class Config:
        from_attributes = True
