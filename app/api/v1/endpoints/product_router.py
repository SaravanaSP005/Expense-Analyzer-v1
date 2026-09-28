from fastapi import APIRouter, Depends, status
from typing import List

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_product_service
from app.schemas.authschema import CurrentUser
from app.schemas.productschema import ProductCreateRequest, ProductResponse, EnableRequest
from app.schemas.response import APIResponse
from app.services.productservice import ProductService
from app.exceptions.exceptions import UnauthorizedException

router = APIRouter(
    prefix="/product",
    tags=["Product"],
)

def _verify_user(current_user: CurrentUser):
    if current_user is None:
        raise UnauthorizedException(message="Invalid user", code="UNAUTHORIZED")

@router.post("/create", response_model=APIResponse[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_product(
    request: ProductCreateRequest, 
    product_service: ProductService = Depends(get_product_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = product_service.product_save(request, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_201_CREATED,
        message="Product created successfully",
        data=result
    )

@router.get("/get", response_model=APIResponse[List[ProductResponse]])
def get_products(
    active: bool | None = None,
    product_service: ProductService = Depends(get_product_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = product_service.product_get(current_user.tenant_id, active)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Products retrieved successfully",
        data=result
    )

@router.put("/{id}", response_model=APIResponse[ProductResponse])
def update_product(
    id: int,
    request: ProductCreateRequest, 
    product_service: ProductService = Depends(get_product_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = product_service.product_update(id, request, current_user.tenant_id, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Product updated successfully",
        data=result
    )

@router.delete("/{id}", response_model=APIResponse[ProductResponse])
def disable_product(
    id: int,
    active: bool = False, 
    product_service: ProductService = Depends(get_product_service),
    current_user: CurrentUser = Depends(get_current_user)
):
    _verify_user(current_user)
    result = product_service.product_enable_disable(id, active, current_user.tenant_id, current_user.user_id)
    return APIResponse(
        success=True,
        statusCode=status.HTTP_200_OK,
        message="Product status updated successfully",
        data=result
    )
