from typing import List
from orange.core.workflow.scheduler import scheduler
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from orange.core.database.database import session
from orange.core.source.model import SubscribeChannel
from orange.dependencies import appDependency
from orange.core.util.series_parser import SeriesParser

from . import subscribe_dao, subscribe_schema

router = APIRouter(tags=["subscribe"], prefix="/subscribe",)


@router.post("/", description="生成订阅")
async def subscribe(vo: subscribe_schema.SubscribeCreate):
    assert (len(vo.source_id) > 0)
    assert (len(vo.provider_id) > 0)
    assert (len(vo.tv_id) > 0)

    rss: SubscribeChannel = appDependency.getSource(
    ).get_rss_detail(vo.source_id, vo.provider_id)
    tv_data = appDependency.getParser().parse_anime_info(vo.tv_id)
    season_data = appDependency.getParser().parse_season_info(vo.tv_id, vo.season_number)

    name = tv_data.get("name")
    status = 0

    subscribe: subscribe_schema.Subscribe = subscribe_schema.Subscribe()
    subscribe.name = name
    subscribe.status = status
    subscribe.source_id = vo.source_id
    subscribe.provider_id = vo.provider_id
    subscribe.tv_id = vo.tv_id
    subscribe.season_number = vo.season_number
    subscribe.parse_param = jsonable_encoder(vo.parse_param)

    subscribe_dao.create_subscribe(session, subscribe)

    try:
        session.add(subscribe)
        session.commit()
        return subscribe
    except:
        session.rollback()
        return f"fail to insert subscribe {subscribe.__repr__()}"


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

    resolve = []

    if (rss):
        for ep in rss.items:
            parser = SeriesParser(subscribe.name)
            parser.unwanted_regexps.append("小剧场")
            parser.parse(ep.title.replace("幻樱字幕组", " "))
            if (parser.episode is not None):
                episode: subscribe_schema.Episode = subscribe_schema.Episode(
                    subscribe_id=subscribe.id, anime_name=subscribe.name, season_number=subscribe.season_number, episode_number=parser.episode)
                try:
                    session.add(episode)
                    session.commit()
                    resolve.append(episode.__repr__())
                except:
                    session.rollback()
                    print(f"fail to insert subscribe {episode.__repr__()}")

    return {
        "id": subscribe.id,
        "name": subscribe.name,
        "resolve": resolve,
    }


def _update_all_subscribe():
    result = []
    for subscribe in session.query(subscribe_schema.Subscribe).all():
        print(f"update subscribe {subscribe.__repr__()}")
        result.append(_update_subscribe(subscribe))
    return result


@router.post("/update/$id", description="执行指定订阅")
async def update_subscribe(id: int):
    qurey = session.query(subscribe_schema.Subscribe).filter(
        subscribe_schema.Subscribe.id == id)
    if qurey.exists:
        return _update_subscribe(qurey.first())
    else:
        return f"no subscribe found by id {id}"


@router.post("/update", description="执行所有订阅")
async def update_all_subscribe():
    return _update_all_subscribe()


scheduler.add_job(_update_all_subscribe, 'interval', minutes=30,
                  id="update_subscribe", replace_existing=True)
