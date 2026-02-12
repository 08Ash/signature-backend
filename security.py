from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET = "super-secret-key"
ALGORITHM = "HS256"

pwd = CryptContext(schemes=["bcrypt"])

def hash_pw(password: str):
    return pwd.hash(password)

def verify_pw(plain, hashed):
    return pwd.verify(plain, hashed)

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=2)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)
