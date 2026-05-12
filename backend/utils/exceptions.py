from enum import Enum


class ErrorCode(str, Enum):
    AI_PROVIDER_ERROR = "AI_PROVIDER_ERROR"
    AI_RESPONSE_PARSE_ERROR = "AI_RESPONSE_PARSE_ERROR"
    AI_TIMEOUT = "AI_TIMEOUT"
    DB_ERROR = "DB_ERROR"
    DB_NOT_FOUND = "DB_NOT_FOUND"
    EXPORT_ERROR = "EXPORT_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class AppException(Exception):
    def __init__(self, code: ErrorCode, message: str, detail: str = ""):
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(message)


class AIProviderException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.AI_PROVIDER_ERROR, message, detail)


class AIResponseParseException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.AI_RESPONSE_PARSE_ERROR, message, detail)


class AITimeoutException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.AI_TIMEOUT, message, detail)


class DatabaseException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.DB_ERROR, message, detail)


class NotFoundException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.DB_NOT_FOUND, message, detail)


class ExportException(AppException):
    def __init__(self, message: str, detail: str = ""):
        super().__init__(ErrorCode.EXPORT_ERROR, message, detail)
