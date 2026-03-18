from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    SECRET_TOKEN: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env")  # ← FIXED

settings = Settings()
