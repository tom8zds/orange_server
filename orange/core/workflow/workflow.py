from fastapi import APIRouter
from orange.core.util.logger import logger
from orange.core.workflow.scheduler import scheduler

router = APIRouter(tags=["workflow"], prefix="/workflow",)

@router.get("/list")
async def jobs():
    jobs = scheduler.get_jobs()
    return [job.id for job in jobs]

@router.get("/purge")
async def purge_jobs():
    scheduler.remove_all_jobs()
    jobs = scheduler.get_jobs()
    return [job.id for job in jobs]