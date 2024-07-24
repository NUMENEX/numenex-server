from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from .database import DatabaseConfig
from .commune import CommuneConfig


class Config(BaseModel):
    database_config: DatabaseConfig
    commune_config: CommuneConfig


class Settings(Config, BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        env_prefix="NUMENEX_",
    )


@lru_cache()
def get_settings():
    return Settings()
