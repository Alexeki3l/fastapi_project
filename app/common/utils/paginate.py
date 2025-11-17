from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def paginate(session: AsyncSession, model, page: int, page_size: int):
    offset = (page - 1) * page_size

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
