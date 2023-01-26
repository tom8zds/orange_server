from enum import IntEnum
from typing import List
from fastapi import APIRouter
from orange.core.database.subscribe_model import Subscribe
from orange.core.database.database import session
from orange.core.source.model import SubscribeChannel
from orange.core.subscribe.model import SubscribeVO
from orange.dependencies import appDependency
from orange.core.util.series_parser import SeriesParser
from orange.core.vo.anime_vo import AnimeVO
from orange.core.util.logger import logger

router = APIRouter(tags=["subscribe"], prefix="/subscribe",)

# @router.get("/",description="根据条件获取订阅")
# async def get_rss_detail(vo.source_id:str, vo.provider_id:str, vo.tv_id:str, season_number:int):
#     assert(len(vo.source_id) > 0)
#     assert(len(vo.provider_id) > 0)
#     assert(len(vo.tv_id) > 0)

#     rss:SubscribeChannel = appDependency.getSource().get_rss_detail(vo.source_id, vo.provider_id)
#     tv_data = appDependency.getParser().parse_anime_info(vo.tv_id)
#     season_data = appDependency.getParser().parse_season_info(vo.tv_id, season_number);

#     result = []

#     if(rss):
#         for ep in rss.items:         
#             parser = SeriesParser(tv_data.get("name") + season_data.get("name"))
#             parser.unwanted_regexps.append("小剧场")
#             try:
#                 parser.parse(ep.title.replace("幻樱字幕组", " "))
#                 result.append({
#                     "name": tv_data.get("name"),
#                     "episode": parser.episode,
#                     "quality": parser.quality.resolution.name,
#                     "subtitle": parser.sub_language
#                 }) 
#             except:
#                 pass
    
#     return result

@router.post("/",description="生成订阅")
async def subscribe(vo: SubscribeVO):
    assert(len(vo.source_id) > 0)
    assert(len(vo.provider_id) > 0)
    assert(len(vo.tv_id) > 0)

    rss:SubscribeChannel = appDependency.getSource().get_rss_detail(vo.source_id, vo.provider_id)
    tv_data = appDependency.getParser().parse_anime_info(vo.tv_id)
    season_data = appDependency.getParser().parse_season_info(vo.tv_id, vo.season_number);

    name = tv_data.get("name") + season_data.get("name")
    status = 0
    quality = 0
    language = 0

    subscribe:Subscribe= Subscribe()
    subscribe.name = name
    subscribe.status = status
    subscribe.source_id = vo.source_id
    subscribe.provider_id = vo.provider_id
    subscribe.tv_id = vo.tv_id
    subscribe.season_number = vo.season_number
    subscribe.quality = quality
    subscribe.language = language
    session.add(subscribe)
    session.commit()
    return subscribe

@router.get("/{id}",description="获取")
async def subscribe(id:int):
   return Subscribe.get_by_id(id)

class SubscribeService:
    def createSubScribe():
        pass