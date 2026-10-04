from functools import cached_property

from config.base_app_settings import BaseAppSettings
from utils.databricks import get_databricks_database_token


class DatabricksSettings(BaseAppSettings):
    """
    Local settings for the application.
    """

    database_resource: str

    @cached_property
    def database_url(self) -> str:
        """
        Get the database URL for Env.DATABRICKS.

        Returns:
            str: The database URL for Env.DATABRICKS.
        """
        token = get_databricks_database_token(endpoint=self.database_resource)
        return f"postgresql+asyncpg://{self.pguser}:{token}@{self.pghost}:{self.pgport}/{self.pgdatabase}?ssl=require"
