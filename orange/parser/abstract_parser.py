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
    def parse_anime_info(tmdv_id:int) -> AnimeVO:
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
    def parse_season_info() -> None:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def parse_episode_info() -> None:
        """
        check api token
        """
                        