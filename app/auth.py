from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.settings import settings

# -------------------------------
# PASSWORD HASHING
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------
# OAUTH2 SCHEME
# -------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------
# FAKE USERS DB
# -------------------------------
fake_users_db = {
    settings.ADMIN_USERNAME: {
        "username": settings.ADMIN_USERNAME,
        "password": settings.ADMIN_PASSWORD       # plain, compared directly at login
    }
}

# -------------------------------
# JWT CONFIG — from .env not hardcoded
# -------------------------------
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -------------------------------
# CREATE TOKEN
# -------------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,                  # ← FIXED from SECRET_KEY
        algorithm=settings.JWT_ALGORITHM          # ← FIXED from hardcoded
    )

# -------------------------------
# VERIFY TOKEN
# -------------------------------
def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,              # ← FIXED
            algorithms=[settings.JWT_ALGORITHM]   # ← FIXED
        )
        return payload
    except JWTError:
        return None