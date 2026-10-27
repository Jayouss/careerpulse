"""CareerPulse Configuration"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "CareerPulse ATS AI Optimizer"
    VERSION: str = "0.1.0"

    PORT: int = 5000
    HOST: str = "0.0.0.0"

    # LLM Provider
    LLM_PROVIDER: str = "mock"  # "openai" | "mock"
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"

    # Match Engine Weights
    KEYWORD_WEIGHT: float = 0.45
    SEMANTIC_WEIGHT: float = 0.55
    DEFAULT_MATCH_THRESHOLD: float = 0.70

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
