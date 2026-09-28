from fastapi import APIRouter, HTTPException, status,Depends
from app.schemas.authschema import LoginRequest,LoginResponse
from app.dependencies.services import get_user_service,get_token_service
from app.services.userservice import UserService
from app.services.tokenservice import TokenService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login",response_model = LoginResponse)
def login(request : LoginRequest,
            user_service: UserService = Depends(get_user_service),
            token_service: TokenService = Depends(get_token_service)):
    
    user = user_service.login_user(request.email,request.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = token_service.create_access_token(user.id,user.tenant_id,user.username)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        tenant_id=user.tenant_id,
        user_name = user.username
    )