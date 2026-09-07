from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    tenant_id: int

class CurrentUser(BaseModel):
    user_id: int
    tenant_id: int