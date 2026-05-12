from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    AI_PROVIDER: Literal["minimax", "openai", "ollama"] = "minimax"
    MINIMAX_API_KEY: str = ""
    MINIMAX_MODEL: str = "MiniMax-M2.7"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "crossborder_ai"
    LOG_LEVEL: str = "INFO"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
