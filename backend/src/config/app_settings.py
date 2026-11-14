import logging
from urllib.parse import urlsplit

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


LOGGER = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    frontend_origins: str
    openai_api_key: SecretStr
    # PostgreSQL fields
    pghost: str
    pgport: int
    pgdatabase: str
    pguser: str
    pgpassword: SecretStr | None = None

    @field_validator("frontend_origins")
    @classmethod
    def validate_frontend_origins(cls, value: str) -> str:
        """
        Ensure configured frontend origins are explicit HTTP(S) origins.

        Args:
            value (str): Comma-separated frontend origins.

        Returns:
            str: The validated frontend origins.

        Raises:
            ValueError: If an origin is a wildcard or contains an invalid URL component.
        """
        origins = [origin.strip() for origin in value.split(",")]
        if not origins or any(not origin for origin in origins):
            raise ValueError("FRONTEND_ORIGINS must contain at least one origin")

        for origin in origins:
            parsed_origin = urlsplit(origin)
            try:
                parsed_origin.port
            except ValueError as error:
                raise ValueError(f"Invalid frontend origin: {origin}") from error

            if (
                origin == "*"
                or parsed_origin.scheme not in {"http", "https"}
                or not parsed_origin.netloc
                or not parsed_origin.hostname
                or parsed_origin.path not in {"", "/"}
                or parsed_origin.query
                or parsed_origin.fragment
                or parsed_origin.username
                or parsed_origin.password
            ):
                raise ValueError(f"Invalid frontend origin: {origin}")

        return value

    @property
    def trusted_frontend_origins(self) -> list[str]:
        """
        Return the configured frontend origins without surrounding whitespace.

        Returns:
            list[str]: The normalized frontend origins.
        """
        return [origin.strip().rstrip("/") for origin in self.frontend_origins.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
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
