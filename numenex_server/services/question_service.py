from .. import schema
import typing as ty

from sqlalchemy.orm import Session
from ..models import Question
from datetime import datetime
from fastapi import HTTPException, status


class QuestionService:
    def create_questions(
        self,
        sess: Session,
        *,
        questions: ty.List[schema.QuestionCreate],
    ):
        db_questions = []
        for question in questions:

            if question.end_date < question.start_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="End date must be after start date",
                )
            if question.end_date < datetime.now().astimezone(question.end_date.tzinfo):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="End date must be in the future",
                )
            if question.start_date < datetime.now().astimezone(
                question.start_date.tzinfo
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be in the future",
                )
            if question.question_type == "multiple_choice":
                if not question.answer_choices or len(question.answer_choices) < 2:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Multiple choice questions must have at least 2 answer choices",
                    )
            db_question = Question(**question.model_dump())
            sess.add(db_question)
            db_questions.append(db_question)
        sess.commit()
        return db_questions

    def get_questions(
        self,
        sess: Session,
    ):
        return (
            sess.query(Question)
            .filter(
                Question.start_date <= datetime.now(),
                Question.end_date >= datetime.now(),
            )
            .all()
        )
