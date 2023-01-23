import uuid as uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin(object):
    uuid: str = Column(UUID(as_uuid=True), default=uuid.uuid4)


class TimestampMixin(object):
    created_at: datetime = Column(DateTime, default=func.now())
