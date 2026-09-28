from sqlalchemy import func
from fastapi import HTTPException, status

from app.models.productdb import ProductEntity
from app.crud.productrepository import ProductRepository
from app.schemas.productschema import ProductCreateRequest


class ProductService:

    def __init__(self, product_repository: ProductRepository):
        self.product_Repository = product_repository

    # Add the Product
    def product_save(self,request_model: ProductCreateRequest) -> ProductEntity | None:

        product_name = request_model.name.lower().replace(" ", "")

        existing_product = self.product_Repository.first(
            func.replace(func.lower(ProductEntity.name)," ","") == product_name,
            ProductEntity.tenant_id == request_model.tenant_id)

        if existing_product is not None:
            raise HTTPException(
                            status_code=status.HTTP_204_NO_CONTENT,
                            detail="Data Not Found.",
                        )


        productentity = self.product_Repository.add(request_model)

        return productentity

    #product get the list tenant based and active
    def product_get(self,tenant_id:int,active : bool) -> ProductEntity | None:
    
            productentity = self.product_Repository.list(ProductEntity.tenant_id == tenant_id,ProductEntity.active == active)
    
            return productentity
    

    # Enable or disable
    def product_enable_disable(self,id: int,active: bool,tenant_id: int) -> ProductEntity | None:

        existing_product = self.product_Repository.first(ProductEntity.id == id,ProductEntity.tenant_id == tenant_id)

        if existing_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data Not Found.",
            )

        existing_product.active = active

        return existing_product
