from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.login.role_permissions import Role_Permissions

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Permissions(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    role_permissions: Mapped[list["Role_Permissions"]] = relationship(
        back_populates="permission"
    )
