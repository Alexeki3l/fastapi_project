from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.common.utils.paginate import paginate
from app.db.session import get_session
from app.schemas.post_schema import PostCreate, PostRead, PostUpdate
from app.models.post import Post, post_tags
from app.models.tag import Tag
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/post", tags=["Posts"])

@router.post("", response_model=PostRead)
async def create_post(payload: PostCreate, session: AsyncSession = Depends(get_session), req_user: User = Depends(get_current_user)):
    new_post = Post(title=payload.title, 
                    content=payload.content, 
                    author_id=req_user.id)
    if payload.tag_ids:
        q = await session.execute(select(Tag).filter(Tag.id.in_(payload.tag_ids), Tag.is_deleted==False))
        tags = q.scalars().all()
        new_post.tags = tags
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    
    q2 = await session.execute(
        select(Post)
        .options(selectinload(Post.tags),selectinload(Post.author) )
        .filter(Post.id == new_post.id)
    )
    post_with_relations = q2.scalar_one()
    return post_with_relations

@router.get("")
async def list_posts(page: int = 1, page_size: int = 10, session: AsyncSession = Depends(get_session)):
    try:
        result = await paginate(session, Post, page, page_size)
        query = await session.execute(
            select(Post)
            .filter(Post.id.in_([p.id for p in result["items"]]))
            .options(
                selectinload(Post.tags),
                selectinload(Post.author)
            )
        )
        posts = query.scalars().all()

        result["items"] = [PostRead.model_validate(p) for p in posts]

        return result
    except HTTPException as e:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    query = await session.execute(
            select(Post)
            .filter(Post.id == post_id, Post.is_deleted==False)
            .options(
                selectinload(Post.tags),
                selectinload(Post.author)
            )
        )
    post = query.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    session: AsyncSession = Depends(get_session),
    req_user: User = Depends(get_current_user)
):
    q = await session.execute(
        select(Post)
        .options(selectinload(Post.tags))
        .filter_by(id=post_id, is_deleted=False)
    )
    post = q.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != req_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    if payload.title is not None:
        post.title = payload.title

    if payload.content is not None:
        post.content = payload.content

    if payload.tag_ids is not None:
        print('===>entra')
        q2 = await session.execute(
            select(Tag).filter(
                Tag.id.in_(payload.tag_ids),
                Tag.is_deleted == False
            )
        )
        post.tags = q2.scalars().all()

    session.add(post)
    await session.commit()

    q3 = await session.execute(
        select(Post)
        .options(selectinload(Post.tags))
        .filter_by(id=post_id)
    )
    updated_post = q3.scalar_one()
    return updated_post

@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session), req_user: User = Depends(get_current_user)):
    q = await session.execute(select(Post).filter_by(id=post_id, is_deleted=False))
    post = q.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != req_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    post.is_deleted = True
    session.add(post)
    await session.commit()
    return {"status": status.HTTP_204_NO_CONTENT, "message": f"Post deleted successfully"}
