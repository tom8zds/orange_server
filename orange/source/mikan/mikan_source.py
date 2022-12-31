from http import HTTPStatus
import re
from typing import List
from orange.source.model import Season, TimeTable, WeekDay,Bangumi
from orange.source.abstract_source import AbstractSource

import bs4

import requests
from urllib.parse import quote

MIKAN_BASE = 'https://mikanani.me'
MIKAN_SEASON = '/Home/BangumiCoverFlowByDayOfWeek'

_SeasonData = {
    Season.SPRING: {
        "ch": "春"
    },
    Season.SUMMER: {
        "ch": "夏"
    },
    Season.AUTUMN: {
        "ch": "秋"
    },
    Season.WINTER: {
        "ch": "冬"
    },
    Season.OTHER: {
        "ch": "OVA"
    }
}

_WeekDay = {
    '星期六': WeekDay.SAT,
    '星期日': WeekDay.SUN,
    '星期一': WeekDay.MON,
    '星期二': WeekDay.TUE,
    '星期三': WeekDay.WED,
    '星期四': WeekDay.THU,
    '星期五': WeekDay.FRI,
    '剧场版': WeekDay.OTH,
    'OVA': WeekDay.OTH,
}


class MikanSource(AbstractSource):

    def update() -> None:
        pass

    def parse_season(self, text: str) -> dict[WeekDay, List[Bangumi]]:

        result: dict[WeekDay, List[Bangumi]] = {}

        soup = bs4.BeautifulSoup(text, "html.parser")
        rowElements = soup.find_all("div", attrs={"class": "sk-bangumi"})

        for row in rowElements:
            titleElem = row.find("div", attrs={"class": "row"})
            if (titleElem != None):
                day = re.sub('\s+', '', titleElem.text)
                weekDay: WeekDay = _WeekDay[day]
                anime_list = row.find_all("li")

                bangumi_list: List[Bangumi] = []
                for anime in anime_list:
                    cover = MIKAN_BASE + anime.find("span").attrs["data-src"]
                    # cover = anime.find("span").attributes("background-image")
                    anime_info = anime.find("div", attrs={"class": "an-info"})
                    anime_info_group = anime_info.find(
                        "div", attrs={"class": "an-info-group"})

                    if (anime_info_group.find("a") is None):
                        anime_name = anime_info_group.find_all("div")[
                            1].attrs["title"]
                    else:
                        anime_name = anime_info_group.find("a").attrs["title"]

                    anime_id = anime.find("span").attrs["data-bangumiid"]

                    bangumi: Bangumi = Bangumi(anime_id, anime_name, cover)

                    bangumi_list.append(bangumi)

                result[weekDay] = bangumi_list
        return result

    def query_season(self, year: int, season: Season) -> tuple[bool, TimeTable]:

        param = "?year={}&seasonStr={}".format(
            year, quote(_SeasonData.get(season).get("ch")))

        url = MIKAN_BASE + MIKAN_SEASON + param

        payload = {}
        headers = {}

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            
            if(response.status_code == HTTPStatus.OK):
                data = self.parse_season(response.text)
                result = TimeTable(year, season, data)
                return [True, result]
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            return [False, err]

        return [False, None]
        
            


         
