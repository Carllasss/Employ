import datetime
from typing import List

from .base import BaseRepository
from schemas.jobs import Job, JobIn
from db.jobs import jobs
from db.users import users

class JobRepository(BaseRepository):

    async def create(self, user_id: int, j: JobIn) -> Job:
        job = Job(
            id=0,
            user_id=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
        )
        values = {**job.dict()}
        values.pop('id', None)
        query = jobs.insert().values(**values)
        job.id = await self.database.execute(query=query)
        return job

    async def update(self, id: int, user_id: int, j: JobIn) -> Job:
        job = Job(
            user_id=user_id,
            updated_at=datetime.datetime.utcnow(),
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
        )
        values = {**job.dict()}
        values.pop('id', None)
        values.pop('created_at', None)
        query = await jobs.update().where(jobs.c.id == id).values(**values)
        job.id = self.database.execute(query=query)
        return job

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Job]:
        query = jobs.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def delete(self, id: int):
        query = jobs.delete().where(jobs.c.id == id)
        return await self.database.execute(query=query)

    async def get_by_id(self, id: int) -> Job:
        query = jobs.select().where(jobs.c.id == id)
        job = await self.database.fetch_one(query=query)
        return Job.parse_obj(job)