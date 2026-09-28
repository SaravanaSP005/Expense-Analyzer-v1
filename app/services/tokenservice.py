from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from app.core.config import settings


class TokenService:

    def create_access_token(
        self,
        user_id: int,
        tenant_id: int,
        user_name : str
    ) -> str:

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "tenant_id": tenant_id,
            "exp": expire,
            "user_name": user_name
        }

        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm
        )

    #GEt Claims
    def verify_token(
        self,
        token: str,
    ) -> dict | None:

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )

            return payload

        except JWTError:
            return None