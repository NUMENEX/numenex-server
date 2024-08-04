from .. import schema
from sqlalchemy.orm import Session
from ..models import SubnetUser


class SubnetUserService:
    def create_user(
        self,
        sess: Session,
        *,
        user: schema.SubnetUserCreate,
    ):
        db_user = self.get_user_using_address(sess, user_address=user.user_address)
        if db_user:
            return db_user
        else:
            new_user = SubnetUser(**user.model_dump())
            sess.add(new_user)
            sess.commit()
            return new_user

    def get_user_using_address(
        self,
        sess: Session,
        *,
        user_address: str,
    ):
        return (
            sess.query(SubnetUser)
            .filter(SubnetUser.user_address == user_address)
            .first()
        )
