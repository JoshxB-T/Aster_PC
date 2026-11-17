from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.login.roles import Roles
    from app.models.login.users import Users

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User_Roles(Base):
    __tablename__ = "user_roles"
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True
    )

    role: Mapped["Roles"] = relationship(
        back_populates="user_roles"
    )
    
    user: Mapped["Users"] = relationship(
        back_populates="user_roles"
    )
