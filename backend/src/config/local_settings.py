from pydantic import SecretStr

from config.base_app_settings import BaseAppSettings


class LocalSettings(BaseAppSettings):
    """
    Local settings for the application.
    """

    pgpassword: SecretStr | None = None

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
