from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.login.users import Users
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
        password_hash = create_account_password_hash(
            credentials.password
        )

        user = Users(
            username=credentials.username,
            email=credentials.email,
            password_hash=password_hash
        )

        session.add(user)
        session.commit()

    except Exception:
        session.rollback()
        raise
