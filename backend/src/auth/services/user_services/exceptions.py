from fastapi import HTTPException, status


class InvalidTokenException(HTTPException):
    """
    Exception raised when the JWT access token is invalid or expired."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UserNotFoundException(HTTPException):
    """
    Exception raised when the user is not found in the database.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )