from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class BaseModel:
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)
