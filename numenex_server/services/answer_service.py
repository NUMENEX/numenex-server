from .. import schema
import typing as ty

from sqlalchemy.orm import Session
from sqlalchemy import select, update, and_
from ..models import Answer, Question
import uuid
from datetime import datetime
from fastapi import HTTPException, status


class AnswerService:
    def create_answers(
        self,
        sess: Session,
        *,
        answers: ty.List[schema.AnswerCreate],
        answerer_id: uuid.UUID,
    ):
        ids = [q.question_id for q in answers]
        now = datetime.now()
        answered_question_ids = select(
            sess.query(Answer.question_id)
            .filter(Answer.answerer_id == answerer_id)
            .subquery()
        )
        questions = (
            sess.query(Question)
            .filter(
                Question.id.in_(ids),
                Question.start_date <= now,
                Question.end_date >= now,
                ~Question.id.in_(answered_question_ids),
            )
            .all()
        )
        if len(questions) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions found for the given question ids or you might have already answered them",
            )
        answered_questions = []
        for question in questions:
            for answer in answers:
                if answer.question_id == question.id:
                    if question.question_type == "multiple_choice":
                        if answer.answer not in question.answer_choices.values():
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Answer {answer.answer} is not in the answer choices for question {question.question}",
                            )
                    sess.add(Answer(**answer.model_dump(), answerer_id=answerer_id))
                    answered_questions.append(question.question)
        sess.commit()
        return {"answered_questions": answered_questions}

    def get_answers(
        self,
        sess: Session,
    ):
        now = datetime.now()
        return (
            sess.query(Answer)
            .join(Question, Answer.question_id == Question.id)
            .filter(
                and_(
                    Question.start_date <= now,
                    Question.end_date >= now,
                )
            )
            .all()
        )

    def update_answer_validations(
        self,
        sess: Session,
        *,
        validations: ty.List[schema.AnswerUpdate],
        module_id: int,
        ss58_address: str,
    ):
        validations_data = []
        for validation in validations:
            validation_data = validation.model_dump()
            validation_data["module_id"] = module_id
            validation_data["ss58_address"] = ss58_address
            validations_data.append(validation_data)

        sess.execute(update(Answer), validations_data)
        sess.commit()
