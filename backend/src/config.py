from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_seconds: int
    openai_api_key: SecretStr
    # Lakebase / PostgreSQL fields
    pghost: str
    pgport: int
    pgdatabase: str
    pguser: str
    databricks_client_secret: SecretStr

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.pguser}:"
            f"{self.databricks_client_secret.get_secret_value()}@"
            f"{self.pghost}:"
            f"{self.pgport}/"
            f"{self.pgdatabase}"
        )


settings = Settings()
