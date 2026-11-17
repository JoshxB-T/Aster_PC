import bcrypt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.login.users import Users


def get_user_by_email(
    session: Session,
    email: str
) -> Users | None:
    statement = (
        select(Users)
        .where(Users.email == email)
    )

    return session.scalars(statement).first()


def verify_password(
    password_attempt: str,
    password_hash: str
) -> bool:
    return bcrypt.checkpw(
        password_attempt.encode('utf-8'),
        password_hash.encode('utf-8')
    )
