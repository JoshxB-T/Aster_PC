import bcrypt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.login.users import Users

def create_account_password_hash(
    password: str
) -> str:
    password_bytes = password.encode('utf-8')
    password_salt = bcrypt.gensalt(rounds=12)

    return bcrypt.hashpw(
        password_bytes,
        password_salt
    ).decode('utf-8')


def check_existing_user_by_email(
    session: Session,
    email: str
) -> bool:
    existing_user = session.scalars(
        select(Users)
        .where(Users.email == email)
    ).first()

    return True if existing_user else False