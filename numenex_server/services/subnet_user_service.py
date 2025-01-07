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
        db_user_using_address = self.get_user_using_address(
            sess, user_address=user.user_address
        )
        if db_user_using_address:
            if (
                db_user_using_address.user_type != user.user_type
                or db_user_using_address.module_id != user.module_id
            ):
                db_user_using_address.user_type = user.user_type
                db_user_using_address.module_id = user.module_id
                sess.commit()
                sess.refresh(db_user_using_address)
            return db_user_using_address

        db_user_using_module_id = self.get_user_module_id(
            sess, module_id=user.module_id
        )
        if db_user_using_module_id:
            if (
                db_user_using_module_id.user_address != user.user_address
                or db_user_using_module_id.user_type != user.user_type
            ):
                db_user_using_module_id.user_address = user.user_address
                db_user_using_module_id.user_type = user.user_type
                sess.commit()
                sess.refresh(db_user_using_module_id)
            return db_user_using_module_id
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

    def get_user_module_id(
        self,
        sess: Session,
        *,
        module_id: int,
    ):
        return sess.query(SubnetUser).filter(SubnetUser.module_id == module_id).first()
