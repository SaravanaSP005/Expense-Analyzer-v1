from decimal import Decimal
from app.schemas.baseschema import BaseRequest,BaseResponse

class ProductCreateRequest(BaseRequest):
    tenant_id: int
    name: str
    amount: Decimal | None = None


class ProductResponse(BaseResponse):
    tenant_id: int
    name: str
    amount: Decimal | None

class EnableRequest():
    id : int 
    active : bool