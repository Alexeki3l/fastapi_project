from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from app.models.mixins import SoftDeleteMixin, TimestampMixin

Base = declarative_base()

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
