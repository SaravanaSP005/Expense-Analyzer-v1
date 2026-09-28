class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        code: str,
        field: str | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.code = code
        self.field = field

        super().__init__(message)

class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Invalid request",
        code: str = "BAD_REQUEST",
        field: str | None = None,
    ):
        super().__init__(
            status_code=400,
            message=message,
            code=code,
            field=field,
        )

class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required",
        code: str = "UNAUTHORIZED",
        field: str | None = None,
    ):
        super().__init__(
            status_code=401,
            message=message,
            code=code,
            field=field,
        )

class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "You do not have permission",
        code: str = "FORBIDDEN",
        field: str | None = None,
    ):
        super().__init__(
            status_code=403,
            message=message,
            code=code,
            field=field,
        )

class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "RESOURCE_NOT_FOUND",
        field: str | None = None,
    ):
        super().__init__(
            status_code=404,
            message=message,
            code=code,
            field=field,
        )

class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
        field: str | None = None,
    ):
        super().__init__(
            status_code=409,
            message=message,
            code=code,
            field=field,
        )

class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Validation error",
        code: str = "VALIDATION_ERROR",
        field: str | None = None,
    ):
        super().__init__(
            status_code=422,
            message=message,
            code=code,
            field=field,
        )

