"""Unit tests for health endpoint, settings, and exception handlers.

This module contains tests for:
    - get_settings() function and caching behavior
    - /health endpoint response structure and content
    - Custom AppException handler and error response format
    - Root endpoint response
"""

from unittest.mock import patch

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.core.exceptions import (
    AgentError,
    AppException,
    ConfigurationError,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    ValidationError,
)
from app.main import app_exception_handler


@pytest.mark.unit
class TestGetSettings:
    """Test suite for get_settings() function.

    The get_settings() function returns a cached Settings instance
    loaded from environment variables using Pydantic Settings.
    """

    def test_get_settings_returns_settings_instance(self) -> None:
        """Test that get_settings() returns a Settings object."""
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_get_settings_returns_cached_instance(self) -> None:
        """Test that get_settings() returns the same cached instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

    def test_get_settings_has_default_values(self) -> None:
        """Test that Settings has expected default values."""
        settings = get_settings()
        assert settings.app_name == "ai-message-writer-assistant"
        assert settings.app_version == "2.0.0"
        assert settings.env == "development"
        assert settings.api_host == "0.0.0.0"
        assert settings.api_port == 8000

    def test_settings_cors_origins_list_property(self) -> None:
        """Test cors_origins_list parses comma-separated origins."""
        settings = get_settings()
        origins = settings.cors_origins_list
        assert isinstance(origins, list)
        assert all(isinstance(origin, str) for origin in origins)
        # Default value from Settings class
        assert "http://localhost:3000" in origins
        assert "http://localhost:5173" in origins

    def test_settings_has_claude_config(self) -> None:
        """Test that Settings has Claude configuration.

        Note: No API key needed - uses Claude Code local setup.
        """
        settings = get_settings()
        assert hasattr(settings, "default_model")
        assert settings.default_model == "sonnet"
        assert hasattr(settings, "max_tokens")
        assert settings.max_tokens == 4096
        assert hasattr(settings, "temperature")
        assert settings.temperature == 1.0

    def test_settings_has_data_paths(self) -> None:
        """Test that Settings has data directory paths."""
        settings = get_settings()
        assert settings.data_dir == "./data"
        assert settings.conversations_dir == "./data/conversations"
        assert settings.settings_dir == "./data/settings"
        assert settings.cache_dir == "./data/cache"

    def test_settings_has_logging_config(self) -> None:
        """Test that Settings has logging configuration."""
        settings = get_settings()
        assert settings.log_level == "INFO"
        assert settings.log_file == "./logs/app.log"

    def test_settings_has_performance_config(self) -> None:
        """Test that Settings has performance configuration."""
        settings = get_settings()
        assert settings.max_parallel_agents == 5
        assert settings.agent_timeout_seconds == 120
        assert settings.cache_enabled is True
        assert settings.cache_ttl_seconds == 3600

    @patch.dict(
        "os.environ",
        {
            "APP_NAME": "test-app",
            "ENV": "test",
            "API_PORT": "9000",
        },
        clear=False,
    )
    def test_settings_loads_from_environment(self) -> None:
        """Test that Settings can be overridden by environment variables."""
        # Clear the cache to force reload
        get_settings.cache_clear()

        settings = get_settings()
        assert settings.app_name == "test-app"
        assert settings.env == "test"
        assert settings.api_port == 9000

        # Cleanup: clear cache again for other tests
        get_settings.cache_clear()


@pytest.mark.unit
class TestHealthEndpoint:
    """Test suite for /health endpoint.

    The health endpoint returns status information for monitoring
    and load balancers.
    """

    def test_health_endpoint_returns_200(self, client: TestClient) -> None:
        """Test that /health endpoint returns HTTP 200 status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_response_structure(self, client: TestClient) -> None:
        """Test that /health endpoint returns expected JSON structure."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "version" in data
        assert "environment" in data

    def test_health_endpoint_response_values(self, client: TestClient) -> None:
        """Test that /health endpoint returns correct values."""
        response = client.get("/health")
        data = response.json()

        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"
        assert data["environment"] == "development"

    def test_health_endpoint_content_type(self, client: TestClient) -> None:
        """Test that /health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_is_async(self, client: TestClient) -> None:
        """Test that /health endpoint can be called multiple times."""
        # Make multiple requests to verify endpoint is working
        responses = [client.get("/health") for _ in range(3)]
        assert all(r.status_code == 200 for r in responses)
        assert all(r.json()["status"] == "healthy" for r in responses)


@pytest.mark.unit
class TestRootEndpoint:
    """Test suite for / (root) endpoint.

    The root endpoint provides basic API information.
    """

    def test_root_endpoint_returns_200(self, client: TestClient) -> None:
        """Test that root endpoint returns HTTP 200 status."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_response_structure(self, client: TestClient) -> None:
        """Test that root endpoint returns expected JSON structure."""
        response = client.get("/")
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "docs" in data

    def test_root_endpoint_response_values(self, client: TestClient) -> None:
        """Test that root endpoint returns correct values."""
        response = client.get("/")
        data = response.json()

        assert data["name"] == "ai-message-writer-assistant"
        assert data["version"] == "2.0.0"
        assert data["docs"] == "/api/docs"

    def test_root_endpoint_content_type(self, client: TestClient) -> None:
        """Test that root endpoint returns JSON content type."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


@pytest.mark.unit
class TestAppExceptionHandler:
    """Test suite for custom AppException handler.

    The exception handler converts AppException instances into
    JSON responses with appropriate status codes.
    """

    async def test_app_exception_handler_basic(self) -> None:
        """Test that exception handler returns correct JSON structure."""
        exc = AppException(
            message="Test error",
            status_code=500,
            error_type="TEST_ERROR",
            details={"key": "value"},
        )

        # Create a mock request
        request = Request({"type": "http", "method": "GET", "url": "http://test"})

        response = await app_exception_handler(request, exc)

        assert response.status_code == 500
        assert response.body is not None

        # Parse JSON from response body
        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "TEST_ERROR"
        assert body["message"] == "Test error"
        assert body["details"] == {"key": "value"}

    async def test_app_exception_handler_not_found(self) -> None:
        """Test exception handler with NotFoundError."""
        exc = NotFoundError(
            message="Resource not found",
            details={"resource_id": "123"},
        )

        request = Request({"type": "http", "method": "GET", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 404

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "NOT_FOUND"
        assert body["message"] == "Resource not found"
        assert body["details"]["resource_id"] == "123"

    async def test_app_exception_handler_validation_error(self) -> None:
        """Test exception handler with ValidationError."""
        exc = ValidationError(
            message="Validation failed",
            details={"field": "email", "reason": "Invalid format"},
        )

        request = Request({"type": "http", "method": "POST", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 422

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "VALIDATION_ERROR"
        assert body["message"] == "Validation failed"
        assert "field" in body["details"]

    async def test_app_exception_handler_conflict_error(self) -> None:
        """Test exception handler with ConflictError."""
        exc = ConflictError(
            message="Resource already exists",
            details={"conversation_id": "abc-123"},
        )

        request = Request({"type": "http", "method": "POST", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 409

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "CONFLICT"
        assert body["message"] == "Resource already exists"

    async def test_app_exception_handler_agent_error(self) -> None:
        """Test exception handler with AgentError."""
        exc = AgentError(
            message="Agent execution failed",
            details={"agent": "MessageParser", "reason": "Timeout"},
        )

        request = Request({"type": "http", "method": "POST", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 500

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "AGENT_ERROR"
        assert body["message"] == "Agent execution failed"

    async def test_app_exception_handler_configuration_error(self) -> None:
        """Test exception handler with ConfigurationError."""
        exc = ConfigurationError(
            message="Missing API key",
            details={"config_key": "ANTHROPIC_API_KEY"},
        )

        request = Request({"type": "http", "method": "GET", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 500

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "CONFIGURATION_ERROR"
        assert body["message"] == "Missing API key"

    async def test_app_exception_handler_external_service_error(self) -> None:
        """Test exception handler with ExternalServiceError."""
        exc = ExternalServiceError(
            message="Anthropic API error",
            details={"service": "Anthropic", "error_code": "rate_limit"},
        )

        request = Request({"type": "http", "method": "POST", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        assert response.status_code == 502

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "EXTERNAL_SERVICE_ERROR"
        assert body["message"] == "Anthropic API error"

    async def test_app_exception_handler_empty_details(self) -> None:
        """Test exception handler with no details provided."""
        exc = AppException(
            message="Error without details",
            status_code=500,
            error_type="GENERIC_ERROR",
        )

        request = Request({"type": "http", "method": "GET", "url": "http://test"})
        response = await app_exception_handler(request, exc)

        import json

        assert isinstance(response.body, bytes)
        body = json.loads(response.body.decode())
        assert body["error"] == "GENERIC_ERROR"
        assert body["message"] == "Error without details"
        assert body["details"] == {}

    def test_app_exception_integration_via_endpoint(self, client: TestClient) -> None:
        """Test that AppException is properly handled by the FastAPI app.

        This test verifies the exception handler works in the context
        of the FastAPI application by triggering an exception through
        a test endpoint.
        """
        # Create a temporary test endpoint that raises an exception
        from app.main import app as test_app

        @test_app.get("/test-exception")
        async def test_exception_endpoint():
            raise NotFoundError(
                message="Test resource not found",
                details={"test_id": "999"},
            )

        response = client.get("/test-exception")

        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "NOT_FOUND"
        assert data["message"] == "Test resource not found"
        assert data["details"]["test_id"] == "999"


@pytest.mark.unit
class TestAppExceptionClasses:
    """Test suite for AppException subclasses.

    Verify that all exception classes are properly configured with
    correct default values.
    """

    def test_app_exception_defaults(self) -> None:
        """Test AppException default values."""
        exc = AppException("Test message")
        assert exc.message == "Test message"
        assert exc.status_code == 500
        assert exc.error_type == "INTERNAL_ERROR"
        assert exc.details == {}

    def test_not_found_error_defaults(self) -> None:
        """Test NotFoundError has correct defaults."""
        exc = NotFoundError()
        assert exc.message == "Resource not found"
        assert exc.status_code == 404
        assert exc.error_type == "NOT_FOUND"
        assert exc.details == {}

    def test_validation_error_defaults(self) -> None:
        """Test ValidationError has correct defaults."""
        exc = ValidationError()
        assert exc.message == "Validation failed"
        assert exc.status_code == 422
        assert exc.error_type == "VALIDATION_ERROR"
        assert exc.details == {}

    def test_conflict_error_defaults(self) -> None:
        """Test ConflictError has correct defaults."""
        exc = ConflictError()
        assert exc.message == "Resource conflict"
        assert exc.status_code == 409
        assert exc.error_type == "CONFLICT"
        assert exc.details == {}

    def test_agent_error_defaults(self) -> None:
        """Test AgentError has correct defaults."""
        exc = AgentError()
        assert exc.message == "Agent execution failed"
        assert exc.status_code == 500
        assert exc.error_type == "AGENT_ERROR"
        assert exc.details == {}

    def test_configuration_error_defaults(self) -> None:
        """Test ConfigurationError has correct defaults."""
        exc = ConfigurationError()
        assert exc.message == "Configuration error"
        assert exc.status_code == 500
        assert exc.error_type == "CONFIGURATION_ERROR"
        assert exc.details == {}

    def test_external_service_error_defaults(self) -> None:
        """Test ExternalServiceError has correct defaults."""
        exc = ExternalServiceError()
        assert exc.message == "External service error"
        assert exc.status_code == 502
        assert exc.error_type == "EXTERNAL_SERVICE_ERROR"
        assert exc.details == {}

    def test_exception_with_custom_message_and_details(self) -> None:
        """Test exception with custom message and details."""
        exc = NotFoundError(
            message="Custom message",
            details={"field1": "value1", "field2": 123},
        )
        assert exc.message == "Custom message"
        assert exc.details["field1"] == "value1"
        assert exc.details["field2"] == 123

    def test_exception_inheritance(self) -> None:
        """Test that all custom exceptions inherit from AppException."""
        assert issubclass(NotFoundError, AppException)
        assert issubclass(ValidationError, AppException)
        assert issubclass(ConflictError, AppException)
        assert issubclass(AgentError, AppException)
        assert issubclass(ConfigurationError, AppException)
        assert issubclass(ExternalServiceError, AppException)

    def test_exception_is_exception(self) -> None:
        """Test that AppException inherits from base Exception."""
        exc = AppException("Test")
        assert isinstance(exc, Exception)
        assert issubclass(AppException, Exception)
