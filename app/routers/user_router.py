from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.common.utils.paginate import paginate
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def get_users(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_session)):
    try:
        result = await paginate(db, User, page, page_size)
        result["items"] = [UserRead.model_validate(user) for user in result["items"]]
        return result
    except HTTPException as e:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.post("", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        db_user = User(email=user.email, password=user.password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id, User.is_deleted == False))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_deleted = True
    await db.commit()
    return {"message": "User deleted"}


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id, User.is_deleted == False))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)
    excluded_fields = ["id",  "created_at", "updated_at", "is_deleted"]
    for key, value in user_data.items():
        if key not in excluded_fields:
            setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user