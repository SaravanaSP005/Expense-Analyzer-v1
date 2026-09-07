from app.schemas.baseschema import BaseRequest,BaseResponse
from app.schemas.userschema import UserCreateRequest
from pydantic import EmailStr

class TenantCreateRequest(BaseRequest):
    tenant_name: str
    contact_number: str
    email: str


class TenantResponse(BaseResponse):
    tenant_name: str
    contact_number: str
    email: str


class TenantWithUserCreateRequest(BaseRequest):
    tenant_name: str
    contact_number: str
    email: EmailStr

    user: UserCreateRequest
