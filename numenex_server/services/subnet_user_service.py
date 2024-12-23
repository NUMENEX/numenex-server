from .. import schema
from sqlalchemy.orm import Session
from ..models import SubnetUser


# subnet user service
class SubnetUserService:
    def create_user(
        self,
        sess: Session,
        *,
        user: schema.SubnetUserCreate,
    ):
        db_user = self.get_user_using_address(sess, user_address=user.user_address)
        if db_user:
            if (
                db_user.user_type != user.user_type
                or db_user.module_id != user.module_id
            ):
                db_user.user_type = user.user_type
                db_user.module_id = user.module_id
                sess.commit()
                sess.refresh(db_user)
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
