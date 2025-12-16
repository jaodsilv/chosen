"""Application configuration management using pydantic-settings."""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    # Lowercase per Python package naming conventions; uppercase "CHOSEN" used for branding
    app_name: str = "chosen"
    app_version: str = "2.0.0"
    env: str = "development"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_url: str = "http://localhost:8000"

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # Claude Configuration (uses Claude Code local setup)
    default_model: str = "sonnet"
    max_tokens: int = 4096
    temperature: float = 1.0

    # Data Paths
    data_dir: str = "./data"
    conversations_dir: str = "./data/conversations"
    settings_dir: str = "./data/settings"
    cache_dir: str = "./data/cache"

    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"

    # Performance
    max_parallel_agents: int = 5
    agent_timeout_seconds: int = 120
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
