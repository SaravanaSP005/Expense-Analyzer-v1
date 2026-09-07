from sqlalchemy.orm import Session
from app.crud.repository_factory import RepositoryFactory


class UnitOfWork:

    def __init__(self, db: Session):
        self.db = db

        factory = RepositoryFactory(db)
        self.users = factory.users
        

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, entity) -> None:
        self.db.refresh(entity)
