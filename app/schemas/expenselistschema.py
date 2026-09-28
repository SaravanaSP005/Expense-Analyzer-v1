from app.schemas.baseschema import BaseRequest,BaseResponse
from decimal import Decimal
from app.schemas.expensedetails import ExpenseDetailsCreateRequest

class ExpenseListCreateRequest(BaseRequest):
    tenant_id: int
    expense_config_id: int
    product_id: int
    quantity: int
    amount: Decimal
    expense_details: ExpenseDetailsCreateRequest


class ExpenseListResponse(BaseResponse):
    tenant_id: int
    expense_config_id: int
    product_id: int
    quantity: int
    amount: Decimal
    
