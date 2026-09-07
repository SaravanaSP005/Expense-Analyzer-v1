from sqlalchemy.orm import Session

from app.crud.userrepository import UserRepository



class RepositoryFactory:

    def __init__(self, db: Session):
        self.db = db

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.db)

    # @property
    # def tenants(self) -> TenantRepository:
    #     return TenantRepository(self.db)

    # @property
    # def products(self) -> ProductRepository:
    #     return ProductRepository(self.db)

    # @property
    # def expenses(self) -> ExpenseRepository:
    #     return ExpenseRepository(self.db)
