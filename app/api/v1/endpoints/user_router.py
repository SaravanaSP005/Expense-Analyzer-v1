from fastapi import APIRouter, Depends, status
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_user_service
from app.schemas.authschema import CurrentUser
from app.schemas.userschema import UserCreateRequest, UserResponse
from app.schemas.response import APIResponse
from app.services.userservice import UserService
from app.exceptions.exceptions import UnauthorizedException

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def _verify_user(current_user: CurrentUser):
    if current_user is None:
        raise UnauthorizedException(message="Invalid user", code="UNAUTHORIZED")

@router.post("/create", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreateRequest, 
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = user_service.create_user(request)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_201_CREATED,
        message="User created successfully",
        data=result
    )

@router.put("/{id}", response_model=APIResponse[UserResponse])
def update_user(
    id: int,
    request: UserCreateRequest, 
    user_service: UserService = Depends(get_user_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = user_service.update_user(id, request)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="User updated successfully",
        data=result
    )
