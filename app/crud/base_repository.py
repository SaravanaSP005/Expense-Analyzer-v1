from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.basedb import BaseEntity


T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):

    def __init__(self, db: Session):
        self.db = db

    def add(self, entity: T) -> T:
        self.db.add(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, entity: T) -> T:
        self.db.refresh(entity)
        return entity

    def first(self,*conditions: Any) -> T | None:

        stmt = (
            select(T)
            .where(*conditions)
            .limit(1)
        )

        return self.db.scalar(stmt)

    def list(self,*conditions: Any) -> list[T]:

        stmt = select(T).where(*conditions)

        return list(
            self.db.scalars(stmt).all()
        )
