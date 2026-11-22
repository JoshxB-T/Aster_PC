from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.login.users import Users
from app.models.login.roles import Roles
from app.models.login.user_roles import User_Roles
from app.services.signup import (
    create_account_password_hash,
    check_existing_user_by_email
)
from app.schemas.signup import SignupRequest

router = APIRouter(
    prefix="/signup",
    tags=["signup"],
)

@router.post(
    "",
)
def signup(
    credentials: SignupRequest,
    session: Session = Depends(get_db),
) -> None:
    if check_existing_user_by_email(session, credentials.email):
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    try:
        regular_user_role = session.scalar(
            select(Roles)
            .where(
                Roles.name == "regular_user"
            )
        )

        if not regular_user_role:
            raise RuntimeError(
                "The regular_user role has not been configured."
            )
        
        password_hash = create_account_password_hash(
            credentials.password
        )

        user = Users(
            username=credentials.username,
            email=credentials.email,
            password_hash=password_hash
        )

        session.add(user)

        # Generate the user's db ID
        session.flush()
        
        user_role = User_Roles(
            user_id=user.id,
            role_id=regular_user_role.id
        )

        session.add(user_role)
        session.commit()

    except Exception:
        session.rollback()
        raise
