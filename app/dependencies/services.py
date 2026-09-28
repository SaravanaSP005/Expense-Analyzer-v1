from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.userrepository import UserRepository
from app.crud.productrepository import ProductRepository
from app.crud.expenserepository import ExpenseRepository
from app.services.userservice import UserService
from app.services.productservice import ProductService
from app.services.tokenservice import TokenService
from app.services.tenantservice import TenantSerivice
from app.services.expenseservice import ExpenseService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository=user_repository,)


def get_token_service() -> TokenService:
    return TokenService()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    product_repository = ProductRepository(db)
    return ProductService(product_repository=product_repository)

def get_tenant_service(db: Session = Depends(get_db)) -> TenantSerivice:
    product_repository = TenantSerivice(db)
    return TenantSerivice(product_repository=product_repository)

def get_expenselist_service(db: Session = Depends(get_db)) -> ExpenseService:
    expense_list_repository = ExpenseRepository(db)
    return ExpenseService(expense_repository=expense_list_repository)

def get_expense_config_service(db: Session = Depends(get_db)) -> ExpenseService:
    product_repository = TenantSerivice(db)
    return TenantSerivice(product_repository=product_repository)
    
