import logging
import os
from enum import StrEnum
from functools import cached_property
from databricks.sdk import WorkspaceClient

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LOGGER = logging.getLogger(__name__)


class Env(StrEnum):
    """
    Enum for the app environment type.
    """

    LOCAL = "local"
    DATABRICKS = "databricks"


class Settings(BaseSettings):
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
    pgpassword: SecretStr | None = None

    @model_validator(mode="after")
    def validate_password(self):
        """
        Validate that the PGPASSWORD is provided for Env.LOCAL.

        Raises:
            ValueError: If PGPASSWORD is not provided when Env.LOCAL.
        """
        if self.env == Env.LOCAL and self.pgpassword is None:
            raise ValueError("PGPASSWORD not provided for Env.LOCAL")
        return self

    @cached_property
    def database_url(self) -> str:
        """
        Get the database URL based on the env value.

        Returns:
            str: The database URL.

        Raises:
            ValueError: If the env value is not recognized.
        """
        LOGGER.warning("Getting database url for env=%s", self.env)
        match self.env:
            case Env.LOCAL:
                return self._local_database_url()
            case Env.DATABRICKS:
                return self._databricks_database_url()
            case _:
                raise ValueError(f"No database url for env: {settings.env}")

    def _local_database_url(self) -> str:
        """
        Get the database URL for Env.LOCAL.

        Returns:
            str: The database URL for Env.LOCAL.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.pguser}:"
            f"{self.pgpassword.get_secret_value()}"
            f"@{self.pghost}:"
            f"{self.pgport}/"
            f"{self.pgdatabase}"
        )

    def _databricks_database_url(self) -> str:
        """
        Get the database URL for Env.DATABRICKS.

        Returns:
            str: The database URL for Env.DATABRICKS.
        """
        token = _get_databricks_database_token()
        return f"postgresql+asyncpg://{self.pguser}:{token}@{self.pghost}:{self.pgport}/{self.pgdatabase}?ssl=require"


def _get_databricks_database_token() -> str:
    """
    Get the database token for Databricks.

    Returns:
        str: The database token.

    Raises:
        RuntimeError: If unable to obtain the database credential or if the token is empty.
    """
    try:
        LOGGER.warning(
            "Connecting to Lakebase host=%s db=%s user=%s",
            settings.pghost,
            settings.pgdatabase,
            settings.pguser,
        )

        client = WorkspaceClient()
        endpoint = os.getenv("DATABASE_RESOURCE")
        if not endpoint:
            raise RuntimeError("DATABASE_RESOURCE environment variable is not set")
        LOGGER.warning("Getting Lakebase database credential for endpoint=%s", endpoint)
        cred = client.postgres.generate_database_credential(endpoint=endpoint)
        if not cred.token:
            raise RuntimeError("Lakebase database credential is empty")
        return cred.token

    except Exception as exc:
        raise RuntimeError("Unable to obtain Lakebase database credential") from exc


settings = Settings()
