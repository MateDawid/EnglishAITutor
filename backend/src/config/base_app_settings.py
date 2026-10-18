import logging
from enum import StrEnum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from abc import ABC, abstractmethod


LOGGER = logging.getLogger(__name__)


class Env(StrEnum):
    """
    Enum for the app environment type.
    """

    LOCAL = "local"
    DATABRICKS = "databricks"


class BaseAppSettings(BaseSettings, ABC):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Env
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_seconds: int
    openai_api_key: SecretStr
    # Lakebase / PostgreSQL fields
    pghost: str
    pgport: int
    pgdatabase: str
    pguser: str

    @property
    @abstractmethod
    def database_url(self) -> str:
        """Database connection URL."""
        raise NotImplementedError


class Env(StrEnum):
    LOCAL = "local"
    DATABRICKS = "databricks"
