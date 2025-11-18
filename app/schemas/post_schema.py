from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from app.schemas.tag_schema import TagRead
from app.schemas.user_schema import UserRead

class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(..., min_length=3, max_length=255)
    content: Optional[str] = None

class PostCreate(PostBase):
    tag_ids: List[int] = []

class PostUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str] = None
    content: Optional[str] = None
    tag_ids: Optional[List[int]] = None

class PostRead(PostBase):
    id: int
    author: UserRead
    tags: List[TagRead] = []
    created_at: datetime
    updated_at: datetime