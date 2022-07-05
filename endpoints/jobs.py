from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.user import User
from schemas.jobs import Job, JobIn
from repositories.jobs import JobRepository
from .depends import get_job_repository, get_current_user

router = APIRouter()


@router.get('/', response_model=List[Job])
async def read_jobs(
        limit: int = 100,
        skip: int = 0,
        jobs: JobRepository = Depends(get_job_repository)):
    return await jobs.get_all(limit=limit, skip=skip)


@router.post('/', response_model=Job)
async def create_jobs(
        j: JobIn,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)):
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only companies can create jobs')
    return await jobs.create(user_id=current_user.id, j=j)


@router.patch('/', response_model=Job)
async def update_jobs(
        j: JobIn,
        id: int,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)
):
    job = await jobs.get_by_id(id=id)
    if job is None and job.user_id != current_user.id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')

    return await jobs.update(id=id, user_id=current_user.id, j=j)


@router.delete('/')
async def delete_jobs(
        id: int,
        jobs: JobRepository = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)
):
    not_found_exp = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Job not found')
    job = await jobs.get_by_id(id=id)
    if job is None and job.user_id != current_user.id:
        raise not_found_exp
    result = await jobs.delete(id=id)
    if result is None:
        raise not_found_exp
    return {'status': 'deleted'}
