from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase settings
    supabase_url: str
    supabase_key: str
    database_url: str

    # Application settings
    secret_key: str
    environment: str = "development"

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
