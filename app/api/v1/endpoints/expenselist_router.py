from fastapi import APIRouter, Depends, status
from typing import List

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_expenselist_service
from app.schemas.authschema import CurrentUser
from app.schemas.expenselistschema import ExpenseListCreateRequest, ExpenseListResponse
from app.schemas.response import APIResponse
from app.services.expenseservice import ExpenseService
from app.exceptions.exceptions import UnauthorizedException


router = APIRouter(
    prefix="/expenselist",
    tags=["ExpenseList"],
)

def _verify_user(current_user: CurrentUser):
    if current_user is None:
        raise UnauthorizedException(message="Invalid user", code="UNAUTHORIZED")

@router.post("/create", response_model=APIResponse[ExpenseListResponse], status_code=status.HTTP_201_CREATED)
def create_expenselist(
    request: ExpenseListCreateRequest, 
    expense_list_service: ExpenseService = Depends(get_expenselist_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = expense_list_service.expense_save(request, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_201_CREATED,
        message="Expense list created successfully",
        data=result
    )

@router.get("/get", response_model=APIResponse[List[ExpenseListResponse]])
def get_expense_list(
    active: bool | None = None, 
    expense_list_service: ExpenseService = Depends(get_expenselist_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = expense_list_service.get_expense_list(current_user.tenant_id, active)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Expense lists retrieved successfully",
        data=result
    )

@router.get("/{id}", response_model=APIResponse[ExpenseListResponse])
def get_expense_by_id(
    id: int, 
    expense_list_service: ExpenseService = Depends(get_expenselist_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = expense_list_service.get_expense_by_id(current_user.tenant_id, id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Expense list retrieved successfully",
        data=result
    )

@router.put("/{id}", response_model=APIResponse[ExpenseListResponse])
def update_expense(
    id: int, 
    request: ExpenseListCreateRequest, 
    expense_list_service: ExpenseService = Depends(get_expenselist_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = expense_list_service.update_expense(current_user.tenant_id, id, request, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Expense list updated successfully",
        data=result
    )

@router.delete("/{id}", response_model=APIResponse[ExpenseListResponse])
def disable(
    id: int, 
    active: bool = False, 
    expense_list_service: ExpenseService = Depends(get_expenselist_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = expense_list_service.disable(current_user.tenant_id, id, active, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Expense list status updated successfully",
        data=result
    )
