from app.schemas.baseschema import BaseRequest,BaseResponse
from decimal import Decimal

class ExpenseDetailsCreateRequest(BaseRequest):
    tenant_id: int
    shareholder_id: list


class ExpenseDetailsResponse(BaseResponse):
    tenant_id: int
    expense_list_id: int
    shareholder_id: int
    shareholder_name:str
    amount: Decimal
