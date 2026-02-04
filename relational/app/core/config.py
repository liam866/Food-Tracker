from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/foodtracker.db"
    VECTOR_SERVICE_URL: str = "http://vector:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
