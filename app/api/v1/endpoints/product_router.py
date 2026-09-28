from fastapi import APIRouter, Depends, status,HTTPException
from app.dependencies.auth import get_current_user
from app.dependencies.services import get_product_service
from app.schemas.authschema import CurrentUser
from app.schemas.productschema import ProductCreateRequest, ProductResponse,EnableRequest
from app.services.productservice import ProductService


router = APIRouter(
    prefix="/peoduct",
    tags=["Product"],
)

@router.post("/create",response_model = ProductResponse)
def create_user(request : ProductCreateRequest, product_service : ProductService = Depends(get_product_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )

    return product_service.product_save(request)


@router.post("/update",response_model = ProductResponse)
def create_user(request : ProductCreateRequest, product_service : ProductService = Depends(get_product_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
    return product_service.product_save(request)

@router.post("/enable",response_model = EnableRequest)
def create_user(request : ProductCreateRequest, product_service : ProductService = Depends(get_product_service),current_user: CurrentUser = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
    return product_service.product_enable_disable(request)


    
