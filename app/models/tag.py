from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

from app.db.base import Base

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    posts = relationship("Post", secondary="post_tags", back_populates="tags")
