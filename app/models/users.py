from sqlalchemy import Column, String, Boolean

from app.db.base_model import BaseModel
from app.models.mixins import TimestampMixin


class User(TimestampMixin, BaseModel):
    __tablename__ = 'user'

    phone_number: str = Column(String(16), nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)

    def __str__(self) -> str:
        return f"User: {self.phone_number}"
