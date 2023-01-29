import json
from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from orange.core.database.database import session
from orange.core.source.model import SubscribeChannel
from orange.dependencies import appDependency
from orange.core.util.series_parser import SeriesParser
from orange.core.workflow.scheduler import scheduler

import traceback


from sqlalchemy.exc import IntegrityError

from . import subscribe_dao, subscribe_schema, subscribe_model

router = APIRouter(tags=["subscribe"], prefix="/subscribe",)

"""
{
  "tv_id": "155942",
  "source_id": "2922",
  "provider_id": "382",
  "season_number": 1,
  "parse_param": {
    "name": "万事屋斋藤、到异世界",
    "alt_names": [
      "Benriya Saitou-san, Isekai ni Iku"
    ],
    "unwanted": [
    ],
    "quality": 1,
    "language": 0
  }
}
"""
@router.post("/", description="生成订阅")
async def subscribe(vo: subscribe_schema.SubscribeCreate):
    assert (len(vo.source_id) > 0)
    assert (len(vo.provider_id) > 0)
    assert (len(vo.tv_id) > 0)

    rss: SubscribeChannel = appDependency.getSource(
    ).get_rss_detail(vo.source_id, vo.provider_id)
    tv_data = appDependency.getParser().parse_anime_info(vo.tv_id)
    season_data = appDependency.getParser().parse_season_info(vo.tv_id, vo.season_number)

    assert(rss)
    assert(tv_data)
    assert(season_data)

    if(len(vo.parse_param.name) == 0):
        vo.parse_param.name = rss.title

    try:
        subscribe_dao.create_subscribe(session, vo)
    except IntegrityError as e: 
        return JSONResponse(status_code=500, content={"message": "index constraint failed"})


@router.post("/test", description="测试订阅", response_model=List[subscribe_schema.EpisodeParse])
async def test_subscribe(subscribe: subscribe_schema.SubscribeCreate):
    assert (len(subscribe.source_id) > 0)
    assert (len(subscribe.provider_id) > 0)
    assert (len(subscribe.tv_id) > 0)

    rss: SubscribeChannel = appDependency.getSource().get_rss_detail(
        subscribe.source_id, subscribe.provider_id)
    tv_data = appDependency.getParser().parse_anime_info(subscribe.tv_id)
    if (tv_data is None):
        return "cannot found tv in parser"
    tv_alt_names = appDependency.getParser().parse_anime_altnames(subscribe.tv_id)

    result = []

    if (rss):
        name = rss.title
        for ep in rss.items:
            if (subscribe.parse_param.name):
                name = subscribe.parse_param.name
            parser = SeriesParser(name)
            parser.alternate_names.__add__(tv_alt_names)
            print(ep.title)
            parser.parse(ep.title)
            if (parser.valid):
                resolve = True
                if (parser.sub_language != subscribe.parse_param.language):
                    resolve = False
                if (parser.quality.name != subscribe_schema.qualities[subscribe.parse_param.quality]):
                    resolve = False
                episode: subscribe_schema.EpisodeParse = subscribe_schema.EpisodeParse(
                    anime_name=name, season_number=subscribe.season_number, episode_number=parser.episode, valide=True, resolve=resolve, parser=parser.__str__())
            else:
                episode: subscribe_schema.EpisodeParse = subscribe_schema.EpisodeParse(
                    anime_name=name, season_number=subscribe.season_number, episode_number=0, parser=parser.__str__())

            result.append(episode)

    return result


@router.get("/{id}", description="获取")
async def subscribe(id: int):
    return subscribe_dao.get_subscribe(id)


def _update_subscribe(subscribe: subscribe_schema.Subscribe) -> dict:

    rss: SubscribeChannel = appDependency.getSource().get_rss_detail(
        subscribe.source_id, subscribe.provider_id)
    tv_data = appDependency.getParser().parse_anime_info(subscribe.tv_id)
    if (tv_data is None):
        return "cannot found tv in parser"
    tv_alt_names = appDependency.getParser().parse_anime_altnames(subscribe.tv_id)
    
    resolve = []
    name = rss.title
    parse_param = json.loads(subscribe.parse_param)

    if (rss):
        for ep in rss.items:
            if (parse_param.get("name")):
                name = parse_param.get("name")
            parser = SeriesParser(name)
            parser.alternate_names.__add__(tv_alt_names)
            print(ep.title)
            parser.parse(ep.title)
            if (parser.valid):
                resolve = True
                if (parser.sub_language != int(parse_param.get("language"))):
                    resolve = False
                if (parser.quality.name != subscribe_schema.qualities[int(parse_param.get("quality"))]):
                    resolve = False

                if (resolve):
                    episode: subscribe_schema.EpisodeCreate = subscribe_schema.EpisodeCreate(
                        subscribe_id=subscribe.id, anime_name=subscribe.name, season_number=subscribe.season_number, episode_number=parser.episode)
                    try:
                        db_item = subscribe_model.Episode(**episode.dict())
                        session.add(db_item)
                        session.commit()
                        session.refresh(db_item)
                        download = appDependency.getDownloader().add_link(ep.torrent, db_item)
                        resolve_detail = download[0].dict()
                        resolve_detail["episode"] = episode.__repr__()
                        resolve.append(resolve_detail)
                    except Exception as e:
                        session.rollback()
                        print(e)
                        traceback.print_exc()
                        print(f"fail to insert subscribe {episode.__repr__()}")

    return {
        "id": subscribe.id,
        "name": subscribe.name,
        "resolve": resolve,
    }


def _update_all_subscribe():
    result = []
    for subscribe in subscribe_dao.get_subscribes(session):
        print(f"update subscribe {subscribe.__repr__()}")
        result.append(_update_subscribe(subscribe))
    return result


@router.post("/update/$id", description="执行指定订阅")
async def update_subscribe(id: int):
    query = subscribe_dao.get_subscribe(session, id)
    if query:
        return _update_subscribe(query)
    else:
        return f"no subscribe found by id {id}"


@router.post("/update", description="执行所有订阅")
async def update_all_subscribe():
    return _update_all_subscribe()


scheduler.add_job(_update_all_subscribe, 'interval', minutes=30,
                  id="update_subscribe", replace_existing=True)
