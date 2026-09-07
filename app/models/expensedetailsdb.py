from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basedb import BaseEntity
from app.models.tenantdb import TenantEntity
from app.models.expenselistdb import ExpenseListEntity
from app.models.userdb import UserEntity


class ExpenseDetails(BaseEntity):
    __tablename__ = "expense_details"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenant.id"),
        nullable=False
    )

    expense_list_id: Mapped[int] = mapped_column(
        ForeignKey("expense_list.id"),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )

    shareholder_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    # Relationships
    tenant: Mapped[TenantEntity] = relationship()

    expense_list: Mapped[ExpenseListEntity] = relationship(
        back_populates="expense_details"
    )

    shareholder: Mapped[UserEntity] = relationship()
