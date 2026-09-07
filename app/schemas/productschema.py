from decimal import Decimal


class ProductCreateRequest(BaseRequest):
    tenant_id: int
    name: str
    amount: Decimal | None = None


class ProductResponse(BaseResponse):
    tenant_id: int
    name: str
    amount: Decimal | None
