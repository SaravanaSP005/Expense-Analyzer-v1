from fastapi import APIRouter, Depends, status,HTTPException
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_tenant_service
from app.schemas.tenantschema import TenantCreateRequest,TenantResponse
from app.services.tenantservice import TenantSerivice


router = APIRouter(
    prefix="/tenant",
    tags=["tenant"],
)

@router.post("/create",response_model = TenantResponse)
def create_user(request : TenantCreateRequest, user_service : TenantSerivice = Depends(get_tenant_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
    return user_service.create_user(request)


@router.post("/update",response_model = TenantResponse)
def create_user(request : TenantCreateRequest, user_service : TenantSerivice = Depends(get_tenant_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
    return user_service.create_user(request)


    
