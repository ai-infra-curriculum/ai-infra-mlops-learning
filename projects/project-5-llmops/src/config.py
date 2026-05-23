"""Pydantic-settings config; reads from env."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_backend_url: str = "http://localhost:8002/v1"
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    chroma_url: str = "http://localhost:8001"
    chroma_collection: str = "docs"
    redis_url: str = "redis://localhost:6379/0"
    llm_rate_limit_per_min: int = 60
    cost_per_1k_input: float = 0.0001
    cost_per_1k_output: float = 0.0003
    semantic_cache_threshold: float = 0.92
    log_level: str = "INFO"
