import re
from typing import List
from fastapi import APIRouter
from orange.dependencies import appDependency

router = APIRouter(tags=["parser"], prefix="/parser",)

from orange.dev_config import parser
from orange.core.parser.abstract_parser import AbstractParser
from orange.parser.tmdb.tmdb_parser import TmdbParser
from orange.core.vo.anime_vo import AnimeVO

@router.get("/search/{bangumi_name}", description="通过番剧名称在刮削库中查找匹配项", response_model=List[AnimeVO])
async def read_item(bangumi_name:str) -> List[AnimeVO]:
    assert(len(bangumi_name) > 3)
    bangumi_name = re.sub("第\w+季", "", bangumi_name, count=0, flags=0)
    return appDependency.getParser().search_anime(bangumi_name)