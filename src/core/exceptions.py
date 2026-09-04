"""Domain and business logic custom exceptions."""


class DairyException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str = "An error occurred.", code: str = "INTERNAL_ERROR", *args, **kwargs):
        super().__init__(message)
        self.message = str(message)
        self.code = code


class DatabaseError(DairyException):
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else kwargs.get("message", "Database operation failed.")
        super().__init__(message=msg, code="DB_ERROR")


class RecordNotFoundError(DairyException):
    def __init__(self, *args, **kwargs):
        entity = args[0] if args else kwargs.get("entity", "Record")
        identifier = args[1] if len(args) > 1 else kwargs.get("identifier", "")
        msg = f"{entity} with identifier '{identifier}' was not found." if identifier else f"{entity} not found."
        super().__init__(message=msg, code="NOT_FOUND")


NotFoundError = RecordNotFoundError


class DuplicateError(DairyException):
    def __init__(self, *args, **kwargs):
        # Accepts any positional args: entity, field, value, etc.
        if len(args) >= 3:
            msg = f"{args[0]} with {args[1]} '{args[2]}' already exists."
        elif args:
            msg = str(args[0])
        else:
            msg = kwargs.get("message", "Record already exists.")
        super().__init__(message=msg, code="DUPLICATE_RECORD")


class ValidationError(DairyException):
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else kwargs.get("message", "Invalid value")
        field = kwargs.get("field", args[1] if len(args) > 1 else "Field")
        self.field = field
        super().__init__(message=f"[{field}] {msg}", code="VALIDATION_ERROR")


class BusinessLogicError(DairyException):
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else kwargs.get("message", "Business logic rule violated.")
        super().__init__(message=msg, code="BUSINESS_RULE_VIOLATION")


class AuthenticationError(DairyException):
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else kwargs.get("message", "Invalid credentials.")
        super().__init__(message=msg, code="AUTH_ERROR")


class InsufficientBalanceError(DairyException):
    def __init__(self, *args, **kwargs):
        msg = args[0] if args else kwargs.get("message", "Insufficient balance for this transaction.")
        super().__init__(message=msg, code="INSUFFICIENT_BALANCE")
