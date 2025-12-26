"""Custom exceptions for the application."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_type: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            status_code: HTTP status code
            error_type: Error type identifier
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details or {}


class NotFoundError(AppException):
    """Resource not found error."""

    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=404,
            error_type="NOT_FOUND",
            details=details,
        )


class ValidationError(AppException):
    """Validation error."""

    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=422,
            error_type="VALIDATION_ERROR",
            details=details,
        )


class ConflictError(AppException):
    """Resource conflict error."""

    def __init__(
        self,
        message: str = "Resource conflict",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=409,
            error_type="CONFLICT",
            details=details,
        )


class AgentError(AppException):
    """AI agent error."""

    def __init__(
        self,
        message: str = "Agent execution failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_type="AGENT_ERROR",
            details=details,
        )


class ConfigurationError(AppException):
    """Configuration error."""

    def __init__(
        self,
        message: str = "Configuration error",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_type="CONFIGURATION_ERROR",
            details=details,
        )


class ExternalServiceError(AppException):
    """External service error (e.g., Anthropic API)."""

    def __init__(
        self,
        message: str = "External service error",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=502,
            error_type="EXTERNAL_SERVICE_ERROR",
            details=details,
        )


# =============================================================================
# File Operation Exceptions
# =============================================================================


class FileOperationError(AppException):
    """Base exception for file operation errors."""

    def __init__(
        self,
        message: str = "File operation failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_type="FILE_OPERATION_ERROR",
            details=details,
        )


class AppFileNotFoundError(FileOperationError):
    """File not found error.

    Note:
        Named AppFileNotFoundError to avoid shadowing Python's built-in
        FileNotFoundError.
    """

    def __init__(
        self,
        message: str = "File not found",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Call AppException.__init__ directly to set correct status code
        AppException.__init__(
            self,
            message=message,
            status_code=404,
            error_type="FILE_NOT_FOUND",
            details=details,
        )


class FileAccessError(FileOperationError):
    """File access denied error (permission issues)."""

    def __init__(
        self,
        message: str = "File access denied",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        AppException.__init__(
            self,
            message=message,
            status_code=403,
            error_type="FILE_ACCESS_DENIED",
            details=details,
        )


class FileLockError(FileOperationError):
    """File lock acquisition failed."""

    def __init__(
        self,
        message: str = "Failed to acquire file lock",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        AppException.__init__(
            self,
            message=message,
            status_code=409,
            error_type="FILE_LOCK_ERROR",
            details=details,
        )


class DirectoryNotFoundError(FileOperationError):
    """Directory not found error."""

    def __init__(
        self,
        message: str = "Directory not found",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        AppException.__init__(
            self,
            message=message,
            status_code=404,
            error_type="DIRECTORY_NOT_FOUND",
            details=details,
        )


class DirectoryNotEmptyError(FileOperationError):
    """Directory not empty error (cannot delete non-empty directory)."""

    def __init__(
        self,
        message: str = "Directory is not empty",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        AppException.__init__(
            self,
            message=message,
            status_code=409,
            error_type="DIRECTORY_NOT_EMPTY",
            details=details,
        )
