from pydantic import BaseModel
import jwt
from .exceptions import UnauthorizedException


class AuthConfig(BaseModel):
    jwt_secret: str
    jwt_algorithm: str


class Auth:
    def __init__(self, config: AuthConfig) -> None:
        self.config = config

    def authenticate(self, token: str):
        admin = jwt.decode(
            token, self.config.jwt_secret, algorithms=[self.config.jwt_algorithm]
        )
        if admin["role"] != "admin":
            raise UnauthorizedException
