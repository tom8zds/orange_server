import abc
from typing import List

from orange.core.vo.anime_vo import AnimeVO


class AbstractParser(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def check_token() -> None:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def search_anime(anime_name:str) -> List[AnimeVO]:
        """
        search anime by name
        """

    @staticmethod
    @abc.abstractmethod
    def parse_anime_info(tv_id:int) -> dict:
        """
        get from 
            data source 
        then
            parse to {Anime} data model
        if valid
            store to database by handler
        """

    @staticmethod
    @abc.abstractmethod
    def parse_anime_altnames(self,tv_id:int) -> List[str]:
        """
        获取中英文名称
        """

    @staticmethod
    @abc.abstractmethod
    def parse_season_info(tv_id:int,season_number:int) -> dict:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def parse_episode_info() -> None:
        """
        check api token
        """
                        