from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    

    ollama_model: str = "llama3.2:3b"

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store_path: str = "data/vector_store"

    top_k: int = 4

    frontend_origin: str = "http://localhost:8501"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()