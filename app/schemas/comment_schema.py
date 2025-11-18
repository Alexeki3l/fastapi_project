from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CommentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    content: str = Field(..., min_length=1, max_length=2000)
    post_id: int

class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
class CommentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    content: Optional[str]=None