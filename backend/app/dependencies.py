"""Dependency injection for FastAPI."""

from app.config import Settings, get_settings


def get_settings_dependency() -> Settings:
    """Dependency that provides application settings."""
    return get_settings()


# Future dependencies will be added here as the application grows:
# - get_conversation_service
# - get_message_service
# - get_agent_orchestrator
# - etc.
