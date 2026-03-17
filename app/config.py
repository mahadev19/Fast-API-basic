from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # -------------------------------
    # Auth
    # -------------------------------
    admin_username: str
    admin_password: str
    secret_token: str

    # -------------------------------
    # JWT
    # -------------------------------
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"

    # -------------------------------
    # Database
    # -------------------------------
    database_url: str

    class Config:
        env_file = ".env"

# Single instance imported across all files
settings = Settings()