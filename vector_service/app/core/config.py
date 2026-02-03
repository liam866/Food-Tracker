from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/foodtracker.db"
    QDRANT_URL: str = "http://qdrant:6333"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OLLAMA_MODEL: str = "all-minilm:22m"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
