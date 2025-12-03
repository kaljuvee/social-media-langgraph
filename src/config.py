"""Configuration management for the social media agent application."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LangSmith Configuration
    langsmith_api_key: Optional[str] = None
    langsmith_tracing_v2: bool = True

    # LLM Configuration
    anthropic_api_key: str

    # Web Scraping
    firecrawl_api_key: str

    # Social Media Authentication
    arcade_api_key: str
    arcade_user_id: str

    # Twitter Configuration
    twitter_api_key: Optional[str] = None
    twitter_api_key_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    twitter_client_id: Optional[str] = None
    twitter_client_secret: Optional[str] = None
    twitter_user_token: Optional[str] = None
    twitter_user_token_secret: Optional[str] = None
    twitter_user_id: Optional[str] = None

    # LinkedIn Configuration
    linkedin_user_id: Optional[str] = None
    linkedin_organization_id: Optional[str] = None
    post_to_linkedin_organization: bool = False

    # Application Configuration
    host: str = "0.0.0.0"
    port: int = 5001
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
