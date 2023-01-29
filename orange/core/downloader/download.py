from typing import List
from fastapi import APIRouter
from orange.core.util.logger import logger
from orange.dependencies import appDependency
from . import dao,schemas
from orange.core.database.database import session

router = APIRouter(tags=["download"], prefix="/download",)

@router.get("/list")
async def get_downloads():
    rows:List[schemas.Download] = dao.get_downloads(session)
    return [schemas.DownloadBase(download.dict()) for download in rows]
    