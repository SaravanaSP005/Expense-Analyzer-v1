from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basedb import BaseEntity
from app.models.tenantdb import TenantEntity
from app.models.userdb import UserEntity


class ExpenseConfigEntity(BaseEntity):
    __tablename__ = "expense_config"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenant.id"),
        nullable=False
    )

    expense_type_id: Mapped[int] = mapped_column(
        nullable=False
    )

    expenser_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        nullable=False
    )

    end_date: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    tenant: Mapped[TenantEntity] = relationship()

    user: Mapped[UserEntity] = relationship()
