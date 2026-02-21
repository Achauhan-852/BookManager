from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.config import get_session
from app.account.models import User
from app.auth_utils import decode_access_token
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/bm/login")

GRACE_SECONDS = 30
async def get_current_user(token: str = Depends(oauth2_scheme),session: AsyncSession = Depends(get_session)):
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    exp_ts = payload.get("exp")
    if not exp_ts:
        raise HTTPException(status_code=401, detail="Token missing exp")
    exp_time = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    if now > exp_time + timedelta(seconds=GRACE_SECONDS):
        raise HTTPException(status_code=401, detail="Token expired")
    user_id = int(payload["sub"])
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
