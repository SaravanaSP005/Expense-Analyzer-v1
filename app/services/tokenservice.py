from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


class TokenService:

    def create_access_token(
        self,
        user_id: int,
        tenant_id: int
    ) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "tenant_id": tenant_id,
            "exp": expire
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
