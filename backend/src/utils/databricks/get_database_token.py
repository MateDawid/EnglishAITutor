import logging
from databricks.sdk import WorkspaceClient


LOGGER = logging.getLogger(__name__)


def get_databricks_database_token(endpoint: str) -> str:
    """
    Get the database token for Databricks.

    Returns:
        str: The database token.

    Raises:
        RuntimeError: If unable to obtain the database credential or if the token is empty.
    """
    try:
        client = WorkspaceClient()
        cred = client.postgres.generate_database_credential(endpoint=endpoint)
        if not cred.token:
            raise RuntimeError("Lakebase database credential is empty")
        return cred.token
    except Exception as exc:
        raise RuntimeError("Unable to obtain Lakebase database credential") from exc
