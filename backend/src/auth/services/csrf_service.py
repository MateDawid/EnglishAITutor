from datetime import UTC, datetime, timedelta

import jwt

from auth.constants import CSRF_TOKEN_EXPIRE_SECONDS
from config import settings


def create_csrf_token() -> str:
    """
    Create a signed CSRF token.

    Returns:
        str: The signed CSRF token.
    """
    expires_at = datetime.now(UTC) + timedelta(seconds=CSRF_TOKEN_EXPIRE_SECONDS)
    return jwt.encode(
        {"purpose": "csrf", "exp": expires_at},
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )


def verify_csrf_token(token: str | None) -> bool:
    """
    Verify that a token is a valid, unexpired CSRF token.

    Args:
        token (str | None): The CSRF token supplied by the request.

    Returns:
        bool: Whether the token is valid.
    """
    if token is None:
        return False

    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "purpose"]},
        )
    except jwt.InvalidTokenError:
        return False

    return payload.get("purpose") == "csrf"
