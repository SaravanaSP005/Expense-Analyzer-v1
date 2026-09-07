from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.basedb import BaseEntity
from app.models.tenantdb import TenantEntity
from app.models.expenseconfig import ExpenseConfigEntity
from app.models.expensedetailsdb import ExpenseDetails
from app.models.productdb import ProductEntity
from app.models.userdb import UserEntity



class ExpenseListEntity(BaseEntity):
    __tablename__ = "expense_list"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenant.id"),
        nullable=False
    )

    expense_config_id: Mapped[int] = mapped_column(
        ForeignKey("expense_config.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )

    create_user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    # Relationships
    tenant: Mapped[TenantEntity] = relationship()

    expense_config: Mapped[ExpenseConfigEntity] = relationship()

    product: Mapped[ProductEntity] = relationship()

    create_user: Mapped[UserEntity] = relationship()

    expense_details: Mapped[list[ExpenseDetails]] = relationship(
        back_populates="expense_list"
    )

