from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.userrepository import UserRepository
from app.services.userservice import UserService
from app.services.tokenservice import TokenService


def get_user_service(db: Session = Depends(get_db),) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository=user_repository,)


def get_token_service() -> TokenService:
    return TokenService()
