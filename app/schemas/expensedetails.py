from app.schemas.baseschema import BaseRequest,BaseResponse
from decimal import Decimal

class ExpenseDetailsCreateRequest(BaseRequest):
    tenant_id: int
    expense_list_id: int
    shareholder_id: int
    amount: Decimal


class ExpenseDetailsResponse(BaseResponse):
    tenant_id: int
    expense_list_id: int
    shareholder_id: int
    amount: Decimal
