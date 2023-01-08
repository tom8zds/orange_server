from enum import IntEnum
from typing import List
from fastapi import APIRouter
from orange.core.source.model import SubscribeChannel
from orange.dependencies import appDependency
from orange.core.util.series_parser import SeriesParser
from orange.core.vo.anime_vo import AnimeVO
from orange.core.util.logger import logger

router = APIRouter(tags=["subscribe"], prefix="/subscribe",)

@router.get("/",description="根据条件获取订阅")
async def get_rss_detail(source_id:str, provider_id:str, db_id:str):
    assert(len(source_id) > 0)
    assert(len(provider_id) > 0)
    assert(len(db_id) > 0)

    rss:SubscribeChannel = appDependency.getSource().get_rss_detail(source_id, provider_id)
    db_data = appDependency.getParser().parse_anime_info(db_id)

    result = []

    if(rss):
        for ep in rss.items:         
            parser = SeriesParser(db_data.get("name"))
            parser.unwanted_regexps.append("小剧场")
            try:
                parser.parse(ep.title.replace("幻樱字幕组", " "))
                result.append({
                    "name": db_data.get("name"),
                    "episode": parser.episode,
                    "quality": parser.quality.resolution.name,
                    "subtitle": parser.sub_language
                }) 
            except:
                pass
    
    return result

class SubscribeService:
    def createSubScribe():
        pass