from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

# -------------------------------
# SECURITY SETUP
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------
# FAKE USERS DB
# — store plain password, hash only at verify time
# -------------------------------
fake_users_db = {
    settings.admin_username: {
        "username": settings.admin_username,
        "password": settings.admin_password        # ← CHANGED: no hashing here
    }
}

# -------------------------------
# PASSWORD HELPERS
# -------------------------------
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)       # still verifies correctly

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# -------------------------------
# JWT TOKEN
# -------------------------------
def create_access_token(data: dict) -> str:
    return jwt.encode(
        data,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )