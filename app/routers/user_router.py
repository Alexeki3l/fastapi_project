from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.common.utils.paginate import paginate
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def get_users(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_session)):
    result = await paginate(db, User, page, page_size)
    result["items"] = [UserRead.model_validate(user) for user in result["items"]]
    return result

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.post("", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
