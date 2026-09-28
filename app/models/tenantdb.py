from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.basedb import BaseEntity

class TenantEntity(BaseEntity):
    __tablename__ = "tenant"

    tenantname : Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    contactnumber : Mapped[str] = mapped_column(
        String(15),
        unique =True,
        nullable=False
    )
    email : Mapped[str] = mapped_column(
        String(15),
        unique =True,
        nullable=False
    )
    
