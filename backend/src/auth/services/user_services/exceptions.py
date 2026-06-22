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

class UserAlreadyExistsException(HTTPException):
    """
    Exception raised when attempting to create a user that already exists.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )


class PasswordMismatchException(HTTPException):
    """
    Exception raised when the provided passwords do not match.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

class InvalidCredentialsException(HTTPException):
    """
    Exception raised when the provided credentials are invalid.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )