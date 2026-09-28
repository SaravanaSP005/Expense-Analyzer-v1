from app.models.expenselistdb import ExpenseListEntity
from app.models.expensedetailsdb import ExpenseDetails
from app.crud.expenserepository import ExpenseRepository
from app.schemas.expenselistschema import ExpenseListCreateRequest
from datetime import datetime, timezone
from app.exceptions.exceptions import NotFoundException, ConflictException, ValidationException

class ExpenseService:
    def __init__(self, expense_repository: ExpenseRepository):
        self.expense_repository = expense_repository

    # Create the Expense and Expense details list
    def expense_save(self, request_model: ExpenseListCreateRequest, user_id: int) -> ExpenseListEntity:
        expense_list = ExpenseListEntity()
        
        if hasattr(request_model, 'id') and request_model.id:
            expense_list.id = request_model.id
            
        expense_list.active = True
        expense_list.tenant_id = request_model.tenant_id
        expense_list.create_user_id = user_id
        expense_list.create_datetime = datetime.now(timezone.utc)
        expense_list.expense_config_id = request_model.expense_config_id
        expense_list.product_id = request_model.product_id
        expense_list.quantity = request_model.quantity
        expense_list.amount = request_model.amount

        # split and save the Share holders Details
        shareholders = request_model.expense_details.shareholder_id
        if not shareholders:
            raise ValidationException(
                message="Shareholders list cannot be empty",
                code="VALIDATION_ERROR",
                field="shareholder_id"
            )
            
        each_person_amount = request_model.amount / len(shareholders)
        
        expense_list.expense_details = []
        for shareholder_id in shareholders:
            expense_detail = ExpenseDetails()
            expense_detail.amount = each_person_amount
            expense_detail.shareholder_id = shareholder_id
            expense_detail.active = True
            expense_detail.create_user_id = user_id
            expense_detail.create_datetime = datetime.now(timezone.utc)
            expense_detail.tenant_id = request_model.tenant_id
            
            expense_list.expense_details.append(expense_detail)

        return self.expense_repository.add(expense_list)

    # Get single Expense List by ID
    def get_expense_by_id(self, tenant_id: int, id: int) -> ExpenseListEntity:
        expense_list = self.expense_repository.first(
            ExpenseListEntity.tenant_id == tenant_id, 
            ExpenseListEntity.id == id
        )
        if expense_list is None:
            raise NotFoundException(
                message="Expense list not found",
                code="EXPENSE_NOT_FOUND",
                field="id",
            )
        return expense_list

    # Get the expense List based on active status
    def get_expense_list(self, tenant_id: int, active: bool | None = None) -> list[ExpenseListEntity]:
        conditions = [ExpenseListEntity.tenant_id == tenant_id]
        if active is not None:
            conditions.append(ExpenseListEntity.active == active)
            
        return self.expense_repository.list(*conditions)

    # Update the Expense List and Expense Details
    def update_expense(self, tenant_id: int, id: int, request_model: ExpenseListCreateRequest, user_id: int) -> ExpenseListEntity:
        expense_list = self.expense_repository.first(
            ExpenseListEntity.tenant_id == tenant_id, 
            ExpenseListEntity.id == id
        )

        if expense_list is None:
            raise NotFoundException(
                message="Expense list not found",
                code="EXPENSE_NOT_FOUND",
                field="id",
            )

        expense_list.expense_config_id = request_model.expense_config_id
        expense_list.product_id = request_model.product_id
        expense_list.quantity = request_model.quantity
        expense_list.amount = request_model.amount
        expense_list.last_user_id = user_id
        expense_list.last_modified = datetime.now(timezone.utc)

        # Update shareholders
        shareholders = request_model.expense_details.shareholder_id
        if not shareholders:
            raise ValidationException(
                message="Shareholders list cannot be empty",
                code="VALIDATION_ERROR",
                field="shareholder_id"
            )

        # For simplicity, we mark old ones as inactive and add new ones
        if expense_list.expense_details:
            for item in expense_list.expense_details:
                item.active = False
                item.last_user_id = user_id
                item.last_modified = datetime.now(timezone.utc)
                
        each_person_amount = request_model.amount / len(shareholders)
        
        for shareholder_id in shareholders:
            expense_detail = ExpenseDetails()
            expense_detail.amount = each_person_amount
            expense_detail.shareholder_id = shareholder_id
            expense_detail.active = True
            expense_detail.create_user_id = user_id
            expense_detail.create_datetime = datetime.now(timezone.utc)
            expense_detail.tenant_id = request_model.tenant_id
            
            expense_list.expense_details.append(expense_detail)

        return self.expense_repository.add(expense_list)

    # Disable the Expense and the Expense Details List
    def disable(self, tenant_id: int, id: int, active: bool, user_id: int) -> ExpenseListEntity:
        expense_list = self.expense_repository.first(
            ExpenseListEntity.tenant_id == tenant_id, 
            ExpenseListEntity.id == id
        )

        if expense_list is None:
            raise NotFoundException(
                message="Expense list not found",
                code="EXPENSE_NOT_FOUND",
                field="id",
            )   
        
        if expense_list.expense_details is not None:
            for item in expense_list.expense_details:
                item.active = active
                item.last_user_id = user_id
                item.last_modified = datetime.now(timezone.utc)

        expense_list.active = active 
        expense_list.last_user_id = user_id
        expense_list.last_modified = datetime.now(timezone.utc)

        return self.expense_repository.add(expense_list)        




