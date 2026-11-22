from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.login.user_activity import User_Activity
    from app.models.login.user_roles import User_Roles

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False 
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    activities: Mapped[list["User_Activity"]] = relationship(
        back_populates="user"
    )

    user_roles: Mapped[list["User_Roles"]] = relationship(
        back_populates="user"
    )