from fastapi import APIRouter, Depends, status,HTTPException
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_expenselist_service
from app.schemas.authschema import CurrentUser
from app.schemas.expenselistschema import ExpenseListCreateRequest, ExpenseListResponse
from app.services.expenseservice import ExpenseService


router = APIRouter(
    prefix="/expenselist",
    tags=["ExpenseList"],
)

@router.post("/create",response_model = ExpenseListResponse)
def create_expenselist(request : ExpenseListCreateRequest, expense_list_service : ExpenseService = Depends(get_expenselist_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )

    return expense_list_service.expense_save(request)

@router.post("/get",response_model = ExpenseListResponse)
def get_expense_list(active : bool | None , expense_list_service : ExpenseService = Depends(get_expenselist_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )

    return expense_list_service.get_expense_list(current_user.tenant_id,active)

@router.post("/disable",response_model = ExpenseListResponse)
def disable(id : int ,active : bool | None , expense_list_service : ExpenseService = Depends(get_expenselist_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )

    return expense_list_service.disable(current_user.tenant_id,active,current_user.)

