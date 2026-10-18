import logging
import os

from .base_app_settings import Env
from .databricks_settings import DatabricksSettings
from .local_settings import LocalSettings

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

try:
    os_env = str(os.environ["ENV"])
except KeyError:
    raise ValueError("ENV environment variable is not set")

try:
    enum_env = Env(os_env.lower())
except ValueError:
    raise ValueError(f"Unsupported ENV value: {os_env}. Use one of: {[e.value for e in Env]}")

match enum_env:
    case Env.LOCAL:
        settings = LocalSettings()
    case Env.DATABRICKS:
        settings = DatabricksSettings()
    case _:
        raise ValueError(f"Settings not created. Unsupported ENV value: {os_env}")

__all__ = ["settings"]
