"""Domain and business logic custom exceptions."""


class DairyException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code


class DatabaseError(DairyException):
    """Raised on database connection or query execution failure."""

    def __init__(self, message: str = "Database operation failed."):
        super().__init__(message=message, code="DB_ERROR")


class RecordNotFoundError(DairyException):
    """Raised when an entity is missing in the database."""

    def __init__(self, entity: str = "Record", identifier: str | int = ""):
        msg = f"{entity} with identifier '{identifier}' was not found." if identifier else f"{entity} not found."
        super().__init__(message=msg, code="NOT_FOUND")


# Alias expected by database repository
NotFoundError = RecordNotFoundError


class DuplicateError(DairyException):
    """Raised when a unique constraint or record already exists."""

    def __init__(self, message: str = "Record already exists."):
        super().__init__(message=message, code="DUPLICATE_RECORD")


class ValidationError(DairyException):
    """Raised when input validation fails."""

    def __init__(self, field: str = "Field", detail: str = "Invalid value"):
        super().__init__(
            message=f"Validation failed for '{field}': {detail}",
            code="VALIDATION_ERROR",
        )


class AuthenticationError(DairyException):
    """Raised on invalid credentials or token failure."""

    def __init__(self, message: str = "Invalid credentials."):
        super().__init__(message=message, code="AUTH_ERROR")


class InsufficientBalanceError(DairyException):
    """Raised during payment attempts when customer/farmer credit is insufficient."""

    def __init__(self, message: str = "Insufficient balance for this transaction."):
        super().__init__(message=message, code="INSUFFICIENT_BALANCE")
