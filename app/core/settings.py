from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # -------------------------------
    # Database
    # -------------------------------
    DATABASE_URL: str

    # -------------------------------
    # Auth
    # -------------------------------
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    SECRET_TOKEN: str

    # -------------------------------
    # JWT
    # -------------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()