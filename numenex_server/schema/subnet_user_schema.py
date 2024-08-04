from pydantic import BaseModel
import typing as ty
from .base_schema import DatabaseMixin


class SubnetUserBase(BaseModel):
    user_address: str
    user_type: ty.Literal["validator", "miner"]


class SubnetUserCreate(SubnetUserBase): ...


class SubnetUser(SubnetUserBase, DatabaseMixin):
    class Config:
        from_attributes = True
