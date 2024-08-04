from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, DateTime, ForeignKey, JSON, UUID, String, ARRAY, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
import uuid


class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    @property
    def created_on(self):
        return self.created_at.date()


class Question(Base):
    __tablename__ = "questions"

    question = Column(String, nullable=False)
    question_type = Column(
        ENUM("multiple_choice", "true_false", "short_answer", name="question_types"),
        nullable=False,
    )
    answer_choices = Column(JSON, nullable=True)
    start_date = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    end_date = Column(DateTime(timezone=True), nullable=False)


class Answer(Base):
    __tablename__ = "answers"

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=False)
    answerer_id = Column(
        UUID(as_uuid=True), ForeignKey("subnet_users.id"), nullable=False
    )
    validations = Column(JSON, nullable=True)
    supporting_resources = Column(JSON, nullable=True)
    miners = relationship("SubnetUser", backref="answers")


class SubnetUser(Base):
    __tablename__ = "subnet_users"

    user_address = Column(String, nullable=False, index=True, unique=True)
    user_type = Column(ENUM("validator", "miner", name="user_types"), nullable=False)
    module_id = Column(Integer, nullable=False, unique=True)
    answers = relationship("Answer", backref="miners")
