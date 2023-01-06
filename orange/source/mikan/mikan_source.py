from http import HTTPStatus
from typing import Callable, TypeVar
from orange.core.util.utils import write_log, write_template
from orange.source.mikan.mikan_define import *
from orange.source.mikan.mikan_parser import MikanParser
from orange.source.model import BangumiDetail, Season, SubscribeChannel, TimeTable
from orange.source.abstract_source import AbstractSource


import requests
from urllib.parse import quote

T = TypeVar("T")

def getRequest(url: str, call_back: Callable[[str], T]) -> tuple[bool, T]:
        payload = {}
        headers = {}
        write_log(url)
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            # response.encoding('utf-8')
            write_log(str(response.status_code))
            
            if(response.status_code == HTTPStatus.OK):
                # write_template(response.text)
                data:T = call_back(response.text)
                return [True, data]
            else:
                return [False, response.status_code]
        except Exception as err:
            write_log(f"Unexpected {err=}, {type(err)=}")
            return [False, err]

class MikanSource(AbstractSource):

    def update() -> None:
        pass

    def query_season(self, year: int, season: Season) -> tuple[bool, TimeTable]:

        param = "?year={}&seasonStr={}".format(
            year, quote(MikanSeasonData.get(season).get("ch")))

        url = MIKAN_BASE + MIKAN_SEASON + param

        return getRequest(url, MikanParser.parse_season)
        
    def get_bangumi_detail(self, bangumi_id:str) -> tuple[bool, BangumiDetail]:
        url = MIKAN_BASE + MIKAN_BANGUMI + "/" + str(bangumi_id)
        

        return getRequest(url, MikanParser.parse_detail)   

    def get_rss_detail(self, bangumi_id:str, provider:str) -> tuple[bool, SubscribeChannel]:
        pass


         
