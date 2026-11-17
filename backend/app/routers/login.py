from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.login import LoginRequest, LoginResponse
from app.services.login import get_user_by_email, verify_password 
from app.core.security import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


def get_db():
    with SessionLocal() as session:
        yield session


@router.post(
    "",
    response_model=LoginResponse
)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_db),
):
    user = get_user_by_email(
        session,
        credentials.email
    )

    if not user or not verify_password(
        credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        subject=user.email
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )