from typing import List
from fastapi import APIRouter
from orange.source.model import Season, TimeTable

from orange.source.mikan.mikan_source import MikanSource
from orange.source.abstract_source import AbstractSource

router = APIRouter(tags=["source"], prefix="/source",)

from orange.dev_config import source

registed_source = {
    "mikan": MikanSource
}

def getSource() -> AbstractSource:
    source_type = registed_source.get(source, MikanSource)
    return source_type()


@router.get("/season/")
async def query_season(year:int, season:Season) -> TimeTable:
    assert(year > 1900)
    flag, data = getSource().query_season(year, season)
    if(flag):
        return data