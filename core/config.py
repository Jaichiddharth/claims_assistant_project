import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM Configuration
    OPENAI_API_KEY: str
    MODEL_REASONING: str = "gpt-4o"
    MODEL_EXTRACTION: str = "gpt-4o-mini"

    # Vector Database (Qdrant)
    QDRANT_URL: str
    QDRANT_API_KEY: str
    COLLECTION_NAME: str = "police_reports"

    # AWS Textract Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"

    # PII Scrubbing Settings
    ENABLE_PII_SCRUBBING: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings to be imported across the project
settings = Settings()