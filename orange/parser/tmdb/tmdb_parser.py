from typing import List
from orange.core.vo.anime_vo import AnimeVO
from orange.core.parser.abstract_parser import AbstractParser

from orange.dev_config import api_key
import tmdbsimple as tmdb

tmdb.API_KEY = api_key

post_basic_url = "https://image.tmdb.org/t/p/original/"

class TmdbParser(AbstractParser):
    def search_anime(self, anime_name:str) -> List[AnimeVO]:
        assert(len(anime_name) > 3)
        search = tmdb.Search()
        response:dict = search.tv (query=anime_name, language="zh", include_adult=True)

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


    def parse_anime_info(self,tv_id:int) -> dict:
        return tmdb.TV(id=tv_id).info(language="zh")

    def parse_anime_altnames(self,tv_id:int) -> dict:
        tv = tmdb.TV(id=tv_id)
        results = tv.alternative_titles(language="zh").get("results") + tv.alternative_titles(language="en").get("results")
        names = []
        for item in results:
            names.append(item.get("title"))

        return names

    def parse_season_info(self,tv_id:int,season_number:int) -> dict:
        return tmdb.TV_Seasons(tv_id=tv_id, season_number=season_number).info(language="zh")
        
    def parse_episode_info() -> None:
        pass