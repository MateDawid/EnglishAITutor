from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from auth.constants import CSRF_TOKEN_HEADER_NAME
from auth.services.csrf_service import verify_csrf_token
from config import settings


class TrustedOriginCSRFMiddleware(BaseHTTPMiddleware):
    """
    Require a trusted origin and signed CSRF token for unsafe HTTP requests.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Validate unsafe requests before passing them to the application.

        Args:
            request (Request): The incoming HTTP request.
            call_next (RequestResponseEndpoint): The next middleware or endpoint.

        Returns:
            Response: The validation error or downstream response.
        """
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            if origin not in settings.trusted_frontend_origins:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Untrusted or missing request origin"},
                )

            csrf_token = request.headers.get(CSRF_TOKEN_HEADER_NAME)
            if not verify_csrf_token(csrf_token):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Missing or invalid CSRF token"},
                )

        return await call_next(request)
