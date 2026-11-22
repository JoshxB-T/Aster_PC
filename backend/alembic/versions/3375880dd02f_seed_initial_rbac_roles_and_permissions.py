"""Seed initial RBAC roles and permissions

Revision ID: 3375880dd02f
Revises: 4dc469784868
Create Date: 2026-11-17 04:11:01.549955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3375880dd02f'
down_revision: Union[str, Sequence[str], None] = '4dc469784868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    connection = op.get_bind()

    # Define existing tables for SQLAlchemy Core operations
    roles = sa.table(
        "roles",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String)
    )
    
    permissions = sa.table(
        "permissions",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String)
    )

    role_permissions = sa.table(
        "role_permissions",
        sa.column("role_id", sa.Integer),
        sa.column("permission_id", sa.Integer)
    )

    # Create roles
    regular_user_id = connection.execute(
        sa.insert(roles)
        .values(name="regular_user")
        .returning(roles.c.id)
    ).scalar_one()

    admin_id = connection.execute(
        sa.insert(roles)
        .values(name="admin")
        .returning(roles.c.id)
    ).scalar_one()

    # Create permissions
    permission_ids = {}

    for permission_name in [
        "parts:create",
        "parts:update",
        "parts:delete"
    ]:
        permission_ids[permission_name] = connection.execute(
            sa.insert(permissions)
            .values(name=permission_name)
            .returning(permissions.c.id)
        ).scalar_one()

    # Assign permissions to regular_user
    connection.execute(
        sa.insert(role_permissions),
        [
            {
                "role_id": regular_user_id,
                "permission_id": permission_ids["parts:create"]
            }
        ]
    )

    # Assign permissions to admin
    connection.execute(
        sa.insert(role_permissions),
        [
            {
                "role_id": admin_id,
                "permission_id": permission_ids["parts:create"]
            },
            {
                "role_id": admin_id,
                "permission_id": permission_ids["parts:update"]
            },
            {
                "role_id": admin_id,
                "permission_id": permission_ids["parts:delete"]
            }
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""

    connection = op.get_bind()

    roles = sa.table(
        "roles",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String)
    )

    permissions = sa.table(
        "permissions",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String)
    )

    role_permissions = sa.table(
        "role_permissions",
        sa.column("role_id", sa.Integer),
        sa.column("permission_id", sa.Integer)
    )

    # Retrieve IDs of seeded roles and permissions
    role_ids = sa.select(roles.c.id).where(
        roles.c.name.in_(["regular_user", "admin"])
    )

    permission_ids = sa.select(permissions.c.id).where(
        permissions.c.name.in_([
            "parts:create",
            "parts:update",
            "parts:delete"
        ])
    )

    # Delete role-permission associations
    connection.execute(
        sa.delete(role_permissions).where(
            role_permissions.c.role_id.in_(role_ids)
        )
    )

    # Delete seeded roles and permissions
    connection.execute(
        sa.delete(roles).where(
            roles.c.name.in_(["regular_user", "admin"])
        )
    )

    connection.execute(
        sa.delete(permissions).where(
            permissions.c.name.in_([
                "parts:create",
                "parts:update",
                "parts:delete"
            ])
        )
    )