# app/models/base.py

from datetime import datetime

from sqlalchemy import DateTime, Integer, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    create_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    create_user: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    last_user: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    last_modified: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now(),
        nullable=True
    )

    row_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )
