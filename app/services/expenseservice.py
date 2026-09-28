from app.models.expenselistdb import ExpenseListEntity
from app.models.expensedetailsdb import ExpenseDetails
from app.crud.expenserepository import ExpenseRepository
from app.schemas.expenselistschema import ExpenseListCreateRequest
from datetime import datetime, timezone
from app.exceptions.exceptions import ( NotFoundException,ConflictException)

class ExpenseService:
    def __int__(self,expense_repository : ExpenseRepository):
        self.expense_repository = expense_repository

    # Add the Expense and Expense details list
    def expense_save(self,request_model:ExpenseListCreateRequest )-> ExpenseListEntity | None:
        expense_details = ExpenseDetails
        expense_list = ExpenseListEntity

        expense_list.id = request_model.id
        expense_list.active = True
        expense_list.tenant_id = request_model.tenant_id
        expense_list.create_user_id = request_model.create_user_id
        expense_list.create_datetime = datetime.now(timezone.utc) 
        expense_list.expense_config_id = request_model.expense_config_id


        #split and save the Share holders Details
        each_person_amount = request_model.amount / request_model.expense_details.shareholder_id.count()
        #calculate of the share holders each preson shares. and create the new response for it.
        
        for item in request_model.expense_details.shareholder_id:
            expense_details.amount = each_person_amount
            expense_details.shareholder_id = item
            expense_details.active = True
            expense_details.create_user_id = request_model.create_user_id
            expense_details.create_datetime = datetime.now(timezone.utc)
            expense_details.tenant_id = request_model.tenant_id
            expense_details.expense_list_id = request_model.id

            expense_list.expense_details = expense_details

        return self.expense_repository.add(expense_list)

    
    # Get teh expense List based active 
    def get_expense_list(self,tenant_Id : int,active : bool | None) ->ExpenseListEntity | None:
        return self.expense_repository.list(ExpenseListEntity.tenant_id == tenant_Id, ExpenseListEntity.active == active)

    

    #disable the Expense and the Expense Details List also. 
    def disable(self,tenant_Id : int,id : int,active : bool,login_user : str) ->ExpenseListEntity | None:

        expense_list = self.expense_repository.first(ExpenseListEntity.tenant_id == tenant_Id, ExpenseListEntity.id == id)

        if expense_list is None:
            raise NotFoundException(
                message="Expense list not found",
                code="EXPENSE_NOT_FOUND",
                field="id",
            )   
        
        if expense_list.expense_details is not None:
            for item in expense_list.expense_details:
                item.active = active
                item.last_user =login_user
                item.last_modified = datetime.now(timezone.utc)

        expense_list.active = active 
        expense_list.last_user = login_user 
        expense_list.last_modified = datetime.now(timezone.utc)


        return self.expense_repository.add(expense_list)


        




