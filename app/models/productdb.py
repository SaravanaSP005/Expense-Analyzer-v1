from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from app.models.basedb import BaseEntity
from app.models.tenantdb import TenantEntity

class ProductEntity(BaseEntity):
    __tablename__ = "product"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenant.id"),
        nullable=False
    )

    name : Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=True
    )


    tenant: Mapped[TenantEntity] = relationship()
