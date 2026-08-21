import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    PROJECT_NAME: str = "CodeSense AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    
    # OpenAI Settings
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini", env="OPENAI_MODEL")
    
    # Storage settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    REPOSITORIES_DIR: Path = BASE_DIR / "repositories"
    
    # Repository cloning configuration
    MAX_CLONE_DEPTH: int = 1
    GIT_TIMEOUT_SECONDS: int = 120
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Ensure repository storage directory exists
settings.REPOSITORIES_DIR.mkdir(parents=True, exist_ok=True)
