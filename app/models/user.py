from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from app.models.mixins import SoftDeleteMixin, TimestampMixin

Base = declarative_base()

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
