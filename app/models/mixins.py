from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import declared_attr

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)

    @declared_attr
    def __table_args__(cls):
        return ()

    def soft_delete(self):
        self.is_deleted = True