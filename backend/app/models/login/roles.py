from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.login.user_roles import User_Roles
    from app.models.login.role_permissions import Role_Permissions

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    user_roles: Mapped[list["User_Roles"]] = relationship(
        back_populates="role"
    )

    role_permissions: Mapped[list["Role_Permissions"]] = relationship(
        back_populates="role"
    )
