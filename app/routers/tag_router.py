from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.common.utils.paginate import paginate
from app.db.session import get_session
from app.schemas.tag_schema import TagCreate, TagRead
from app.models.tag import Tag

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("", response_model=TagRead)
async def create_tag(payload: TagCreate, session: AsyncSession = Depends(get_session)):
    q = await session.execute(select(Tag).filter_by(name=payload.name))
    existing = q.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag(name=payload.name)
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag

@router.get("")
async def list_tags(page: int = 1, page_size: int = 10,session: AsyncSession = Depends(get_session)):
    try:
        result = await paginate(session, Tag, page, page_size)
        result["items"] = [TagRead.model_validate(user) for user in result["items"]]
        return result
    except HTTPException as e:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")