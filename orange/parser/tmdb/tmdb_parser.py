import json
from typing import List
from orange.core.vo.anime_vo import AnimeVO
from orange.parser.abstract_parser import AbstractParser

from orange.dev_config import api_key
import tmdbsimple as tmdb

tmdb.API_KEY = api_key

post_basic_url = "https://image.tmdb.org/t/p/original/"

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

class TmdbParser(AbstractParser):
    def search_anime(self, anime_name:str) -> List[AnimeVO]:
        assert(len(anime_name) > 3)
        search = tmdb.Search()
        response:dict = search.tv (query=anime_name, language="zh", include_adult=True)
        # for s in search.results:
        #     write_log(s['title'], s['id'], s['release_date'], s['popularity'])
        result: List[AnimeVO] = []
        animes: List[dict] = response.get("results")
        for anime in animes:
            tv = tmdb.TV(anime.get("id")).info(language="zh")
            seasons:List[dict] = tv.get("seasons")
            for season in seasons:
                cover = ""
                if season.get("poster_path") is None:
                    cover = anime.get("poster_path")
                else:
                    cover = season.get("poster_path")
                animeVO:AnimeVO = AnimeVO(anime.get("id"),season.get("id"),anime.get("name"), season.get("name"), post_basic_url + cover, season.get("overview"))
                result.append(animeVO)
        return result

    def check_token() -> None:
        assert(len(tmdb.API_KEY) > 0)


    def parse_anime_info(tmdv_id:int) -> AnimeVO:
        pass

    def parse_season_info() -> None:
        pass

    def parse_episode_info() -> None:
        pass