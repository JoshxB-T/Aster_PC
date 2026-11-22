from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.authentication import get_current_user

from app.models.login.users import Users
from app.models.login.roles import Roles
from app.models.login.permissions import Permissions
from app.models.login.user_roles import User_Roles
from app.models.login.role_permissions import Role_Permissions
from app.db.dependencies import get_db


def require_permission(permission_name: str):
    def permission_checker(
        current_user: Users = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        statement = (
            select(Permissions.id)
            .join(
                Role_Permissions,
                Role_Permissions.permission_id == Permissions.id
            )
            .join(
                Roles,
                Roles.id == Role_Permissions.role_id
            )
            .join(
                User_Roles,
                User_Roles.role_id == Roles.id
            )
            .where(
                User_Roles.user_id == current_user.id,
                Permissions.name == permission_name
            )
        )

        permission = db.scalar(statement)
        
        if permission is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return current_user

    return permission_checker