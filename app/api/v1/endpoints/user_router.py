from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_user_service
from app.schemas.authschema import CurrentUser
from app.schemas.userschema import UserCreateRequest, UserResponse
from app.services.userservice import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/create",response_model = UserResponse)
def create_user(request : UserCreateRequest, user_service : UserService = Depends(get_user_service),current_user: CurrentUser = Depends(get_current_user)):

    pass
    
