from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext


# ✅ Configuration
SECRET_KEY = "supersecretkey"  # store in .env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ✅ Initialize password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ----------------------------
# 🔒 Password Hashing & Verify
# ----------------------------
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using argon2.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain text password matches the hashed password.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


# ----------------------------
# 🔑 JWT Token Creation / Decode
# ----------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Decodes and validates a JWT token. Returns the payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
