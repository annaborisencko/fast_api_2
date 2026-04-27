import bcrypt
import jwt
from datetime import datetime, timedelta
from config import ACCESS_TOKEN_EXPIRE_SECONDS, ALGORITHM, SECRET_KEY


def generate_token(user_data: dict, expires_in: int = None):
    if expires_in:
        expire = datetime.utcnow() + timedelta(seconds=expires_in)
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    user_data.update({"exp": expire})
    token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str):
    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return user_data
    except jwt.PyJWTError as e:
        print(f"Token decode error: {e}")
        return None


def hash_password(password: str) -> str:
    password = password.encode()
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hashed.decode()


def check_password(password: str, password_hashed: str) -> bool:
    password = password.encode()
    password_hashed = password_hashed.encode()
    return bcrypt.checkpw(password, password_hashed)