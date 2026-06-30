"""Application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables with sensible defaults."""

    app_name: str = "Document Intelligence API"
    app_version: str = "0.1.0"
    app_description: str = "Backend API for document intelligence and retrieval."

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
