from app.schemas.baseschema import BaseRequest, BaseResponse

class UserCreateRequest(BaseRequest):
    tenant_id: int
    username: str
    email: str
    display_name: str
    password: str

class UserResponse(BaseResponse):
    tenant_id: int
    username: str
    email: str
    displayname: str

class EnableResponse():
    id : int 
    active : bool