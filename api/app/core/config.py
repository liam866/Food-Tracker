from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RELATIONAL_SERVICE_URL: str = "http://relational:8000"
    VISION_SERVICE_URL: str = "http://vision:8000"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434" 
    OLLAMA_MODEL: str = "qwen2.5:0.5b"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
