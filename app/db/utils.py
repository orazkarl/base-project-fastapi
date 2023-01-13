from sqlalchemy import select
from sqlalchemy.orm import Session


def get_or_create_from_db(
        *,
        db: Session,
        data: dict,
        db_model: type,
):
    obj_query = (
        select(db_model)
        .filter(*(getattr(db_model, key) == value for key, value in data.items()))
        .limit(1)
    )
    obj_from_db = db.execute(obj_query).scalars().first()
    if obj_from_db:
        for key, value in data.items():
            setattr(obj_from_db, key, value)
        db.flush()
    else:
        obj_from_db = db_model(**data)
        db.add(obj_from_db)
        db.flush()
    return obj_from_db


def create_object(
        *,
        db: Session,
        data: dict,
        db_model: type
):
    obj_from_db = db_model(**data)
    db.add(obj_from_db)
    db.flush()
    return obj_from_db
