from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.schemas.comment_schema import CommentCreate, CommentRead, CommentUpdate
from app.models.comment import Comment
from app.models.post import Post
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("", response_model=CommentRead)
async def create_comment(payload: CommentCreate, session: AsyncSession = Depends(get_session), req_user: User = Depends(get_current_user)):
    query_post = await session.execute(select(Post).filter_by(id=payload.post_id, is_deleted=False))
    post = query_post.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(content=payload.content, post_id=payload.post_id, author_id=req_user.id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

@router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: int, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(Comment).filter_by(id=comment_id, is_deleted=False))
    comment = query.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.patch("/{comment_id}", response_model=CommentRead)
async def update_comment(comment_id: int, payload: CommentUpdate, session: AsyncSession = Depends(get_session), req_user: User = Depends(get_current_user)):
    q = await session.execute(select(Comment).filter_by(id=comment_id, is_deleted=False))
    comment = q.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != req_user.id:
        qpost = await session.execute(select(Post).filter_by(id=comment.post_id))
        post = qpost.scalar_one_or_none()
        if not post or post.author_id != req_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    comment.content = payload.content
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_session), req_user: User = Depends(get_current_user)):
    q = await session.execute(select(Comment).filter_by(id=comment_id, is_deleted=False))
    comment = q.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != req_user.id:
        qpost = await session.execute(select(Post).filter_by(id=comment.post_id))
        post = qpost.scalar_one_or_none()
        if not post or post.author_id != req_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    comment.is_deleted = True
    session.add(comment)
    await session.commit()
    return {"status": status.HTTP_204_NO_CONTENT, "message": f"Comment deleted successfully"}