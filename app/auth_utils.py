import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return data
