from sqlalchemy import select

from app.models.userdb import UserEntity
from app.crud.base_repository import BaseRepository


class UserRepository(BaseRepository[UserEntity]):

    def get_by_email(self,email: str,tenant_id: int) -> UserEntity | None:

        return self.first(
            UserEntity.email == email,
            UserEntity.tenant_id == tenant_id,
        )
