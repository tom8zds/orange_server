import abc

from orange.model.anime_model import Anime


class AbstractParser(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def check_token() -> None:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def search_anime() -> None:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def parse_anime_info(tmdv_id:int) -> Anime:
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
                        