from typing import List
from fastapi import APIRouter
from orange.core.source.model import BangumiDetail, Season, SubscribeChannel, TimeTable
from orange.dependencies import appDependency

router = APIRouter(tags=["source"], prefix="/source",)

@router.get("/season/", description="根据年份季度获取时间表",response_model=TimeTable)
async def query_season(year:int, season:Season) -> TimeTable:
    assert(year > 1900)
    data = appDependency.getSource().query_season(year, season)
    return data

@router.get("/bangumi/",description="根据番剧id获取番剧信息及字幕组列表",response_model=BangumiDetail)
async def query_bangumi_detail(id:str) -> BangumiDetail:
    assert(len(id) > 0)
    data = appDependency.getSource().get_bangumi_detail(id)
    return data

@router.get("/rss/",description="根据番剧id字幕组id获取rss种子列表",response_model=SubscribeChannel)
async def get_rss_detail(id:str, provider:str) -> SubscribeChannel:
    assert(len(id) > 0)
    assert(len(provider) > 0)
    data = appDependency.getSource().get_rss_detail(id, provider)
    return data