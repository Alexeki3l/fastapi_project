from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def paginate(session: AsyncSession, model, page: int, page_size: int, is_deleted=False):
    offset = (page - 1) * page_size

    if hasattr(model, "is_deleted"):
        total = await session.scalar(
            select(func.count()).select_from(model).where(model.is_deleted == is_deleted)
        )
        query = await session.execute(
            select(model).where(model.is_deleted == is_deleted).offset(offset).limit(page_size)
        )
    else:
        total = await session.scalar(
            select(func.count()).select_from(model)
        )
        query = await session.execute(
            select(model).offset(offset).limit(page_size)
        )

    return {
        "items": query.scalars().all(),
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size
    }
