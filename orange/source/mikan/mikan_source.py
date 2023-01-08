from http import HTTPStatus
import json
from typing import Callable, TypeVar
from orange.core.util.utils import write_log
from orange.source.mikan.mikan_define import *
from orange.source.mikan.mikan_parser import MikanParser
from orange.core.source.model import BangumiDetail, Season, SubscribeChannel, TimeTable
from orange.core.source.abstract_source import AbstractSource

import requests

T = TypeVar("T")


def getRequest(url: str, params: dict, call_back: Callable[[str], T]) -> T:
    payload = {}
    headers = {}
    try:
        response = requests.request(
            "GET", url, params=params, headers=headers, data=payload)
        # response.encoding('utf-8')
        write_log(str(response.status_code))
        write_log(json.dumps(params))
        write_log(response.url)

        if (response.status_code == HTTPStatus.OK):
            # write_template(response.text)
            data: T = call_back(response.text)
            return data
        else:
            return response.status_code
    except Exception as err:
        write_log(f"Unexpected {err=}, {type(err)=}")
        return err


class MikanSource(AbstractSource):

    def update() -> None:
        pass

    def query_season(self, year: int, season: Season) -> TimeTable:

        params: dict = {
            "year": year,
            "seasonStr": MikanSeasonData.get(season).get("ch"),
        }

        url = MIKAN_BASE + MIKAN_SEASON

        data = getRequest(url, params, MikanParser.parse_season)
        return TimeTable(year, season, data)

    def get_bangumi_detail(self, bangumi_id: str) -> BangumiDetail:
        url = MIKAN_BASE + MIKAN_BANGUMI + "/" + str(bangumi_id)
        return getRequest(url, {}, MikanParser.parse_detail)

    def get_rss_detail(self, bangumi_id: str, provider: str) -> SubscribeChannel:
        url = MIKAN_BASE + MIKAN_RSS
        params = {
            "bangumiId": bangumi_id,
            "subgroupid": provider
        }

        return getRequest(url, params, MikanParser.parse_rss_channel)
