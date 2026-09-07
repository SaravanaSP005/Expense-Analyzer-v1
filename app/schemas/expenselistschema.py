class ExpenseListCreateRequest(BaseRequest):
    tenant_id: int
    expense_config_id: int
    product_id: int
    quantity: int
    amount: Decimal


class ExpenseListResponse(BaseResponse):
    tenant_id: int
    expense_config_id: int
    product_id: int
    quantity: int
    amount: Decimal
