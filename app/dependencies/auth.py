from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.services import get_token_service
from app.services.tokenservice import TokenService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    token_service: TokenService = Depends(get_token_service),
):
    payload = token_service.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    user_name = payload.get("user_name")

    if user_id is None or tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    return {
        "user_id": int(user_id),
        "tenant_id": int(tenant_id),
        "user_name": user_name
    }
