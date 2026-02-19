from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.config import get_session
from app.account.models import User
from app.auth_utils import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/bm/login")

async def get_current_user(token: str = Depends(oauth2_scheme),session: AsyncSession = Depends(get_session)):
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user