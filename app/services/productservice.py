from sqlalchemy import func
from app.models.productdb import ProductEntity
from app.crud.productrepository import ProductRepository
from app.schemas.productschema import ProductCreateRequest
from app.exceptions.exceptions import ConflictException, NotFoundException

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_Repository = product_repository

    # Add the Product
    def product_save(self, request_model: ProductCreateRequest, user_id: int) -> ProductEntity:
        product_name = request_model.name.lower().replace(" ", "")

        existing_product = self.product_Repository.first(
            func.replace(func.lower(ProductEntity.name)," ","") == product_name,
            ProductEntity.tenant_id == request_model.tenant_id
        )

        if existing_product is not None:
            raise ConflictException(
                message="Product already exists",
                code="PRODUCT_EXISTS",
                field="name"
            )

        product_data = request_model.model_dump()
        productentity = ProductEntity(**product_data)
        productentity.active = True
        productentity.create_user_id = user_id
        
        return self.product_Repository.add(productentity)

    # product get the list tenant based and active
    def product_get(self, tenant_id: int, active: bool | None = None) -> list[ProductEntity]:
        conditions = [ProductEntity.tenant_id == tenant_id]
        if active is not None:
            conditions.append(ProductEntity.active == active)
            
        return self.product_Repository.list(*conditions)

    # Update Product
    def product_update(self, id: int, request_model: ProductCreateRequest, tenant_id: int, user_id: int) -> ProductEntity:
        existing_product = self.product_Repository.first(ProductEntity.id == id, ProductEntity.tenant_id == tenant_id)
        if existing_product is None:
            raise NotFoundException(message="Product Not Found", code="PRODUCT_NOT_FOUND", field="id")
            
        existing_product.name = request_model.name
        existing_product.amount = request_model.amount
        existing_product.last_user_id = user_id
        
        return self.product_Repository.add(existing_product)

    # Enable or disable
    def product_enable_disable(self, id: int, active: bool, tenant_id: int, user_id: int) -> ProductEntity:
        existing_product = self.product_Repository.first(ProductEntity.id == id, ProductEntity.tenant_id == tenant_id)

        if existing_product is None:
            raise NotFoundException(
                message="Product Not Found",
                code="PRODUCT_NOT_FOUND",
                field="id"
            )

        existing_product.active = active
        existing_product.last_user_id = user_id
        
        return self.product_Repository.add(existing_product)
