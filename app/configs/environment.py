from functools import lru_cache
import os
from pydantic import validator
import logging
from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_URL: str
    DEBUG_MODE: bool
    APP_MAX_PAGE_SIZE: int
    APP_DEFAULT_PAGE_SIZE: int
    APP_DEFAULT_START_INDEX: int
    APP_ADDS_POSITIONS: list[int]
    TEST_WEB_APP_HOST: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@validator("APP_ADDS_POSITIONS", pre=True)
def parse_positions(cls, v):
    if isinstance(v, str):
        return [int(x) for x in v.split(",")]
    return v  # return the value as is if it's not a string


@lru_cache
def get_environment_variables() -> EnvironmentSettings:
    return EnvironmentSettings()
