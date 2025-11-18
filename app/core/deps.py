from fastapi import Depends, HTTPException, status
from app.core.security import oauth2_scheme
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from sqlalchemy import select
from app.models.user import User

import jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(jwt=token, key= settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception
    q = await session.execute(select(User).filter_by(id=user_id, is_deleted=False))
    user = q.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
