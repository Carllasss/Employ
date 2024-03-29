import datetime

import asyncpg.exceptions
from starlette.responses import JSONResponse

from .base import BaseRepository
from db.users import users
from typing import List, Optional
from schemas.user import User, UserIn
from utils.security import verify_password, hash_password


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop('id', None)
        try:
            query = users.insert().values(**values)
            user.id = await self.database.execute(query)
        except asyncpg.exceptions.UniqueViolationError:
            return JSONResponse(content={'error': 'this email is already registered'}, status_code=400)
        return user

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user.dict()}
        values.pop('created_at', None)
        values.pop('id', None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user
