from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./foodtracker.db"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434" 
    OLLAMA_MODEL: str = "qwen2.5:0.5b"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
