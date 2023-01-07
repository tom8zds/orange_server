from typing import List
from fastapi import APIRouter
from orange.source.model import BangumiDetail, Season, SubscribeChannel, TimeTable

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


@router.get("/season/", description="根据年份季度获取时间表",response_model=TimeTable)
async def query_season(year:int, season:Season) -> TimeTable:
    assert(year > 1900)
    flag, data = getSource().query_season(year, season)
    if(flag):
        return data

@router.get("/bangumi/",description="根据番剧id获取番剧信息及字幕组列表",response_model=BangumiDetail)
async def query_bangumi_detail(id:str) -> BangumiDetail:
    assert(len(id) > 0)
    flag, data = getSource().get_bangumi_detail(id)
    return data

@router.get("/rss/",description="根据番剧id字幕组id获取rss种子列表",response_model=SubscribeChannel)
async def get_rss_detail(id:str, provider:str) -> SubscribeChannel:
    assert(len(id) > 0)
    assert(len(provider) > 0)
    flag, data = getSource().get_rss_detail(id, provider)
    return data