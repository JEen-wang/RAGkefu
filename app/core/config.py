"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for RAGkefu.

    Later steps will consume reserved fields (database, redis, etc.)
    without changing the configuration entrypoint.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "RAGkefu"
    app_env: str = "local"
    app_version: str = "0.1.0"
    debug: bool = True
    api_prefix: str = "/v1"

    # Reserved for later steps (safe defaults for local bootstrap)
    database_url: str = "postgresql+asyncpg://ragkefu:ragkefu@localhost:5434/ragkefu"
    redis_url: str = "redis://localhost:6379/0"
    chroma_url: str = "http://localhost:8001"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
