from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead
from app.core.security import hash_password
from app.core.config import settings
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    print("entra")
    q = await session.execute(select(User).filter_by(email=payload.email))
    existing = q.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=payload.email, password=hash_password(payload.password))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user