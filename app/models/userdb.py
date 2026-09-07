from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basedb import BaseEntity
from app.models.tenantdb import TenantEntity


class UserEntity(BaseEntity):
    __tablename__ = "users"

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenant.id"),
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
            String(255),
            nullable=False
        )
        
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    displayname : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tenant: Mapped[TenantEntity] = relationship()