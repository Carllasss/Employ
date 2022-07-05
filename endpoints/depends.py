from fastapi import Depends, HTTPException, status
from repositories.jobs import JobRepository
from repositories.users import UserRepository
from db.base import database
from schemas.user import User
from schemas.jobs import Job
from utils.security import JWTBearer, decode_access_token


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_job_repository() -> JobRepository:
    return JobRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer())
) -> User:
    cred_exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exp

    email: str = payload.get('sub')
    if email is None:
        raise cred_exp

    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exp

    return user
