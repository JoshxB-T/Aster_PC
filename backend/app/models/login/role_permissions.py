from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.login.roles import Roles
    from app.models.login.permissions import Permissions

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Role_Permissions(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True
    )

    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
        primary_key=True
    )

    role: Mapped["Roles"] = relationship(
        back_populates="role_permissions"
    )
        
    permission: Mapped["Permissions"] = relationship(
        back_populates="role_permissions"
    )
