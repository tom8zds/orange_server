import abc

from orange.source.model.time_table import Season, TimeTable

class AbstractSource(metaclass=abc.ABCMeta):
    
    @staticmethod
    @abc.abstractmethod
    def update() -> None:
        """
        check api token
        """

    @staticmethod
    @abc.abstractmethod
    def get_time_table(year:int, season:Season) -> TimeTable:
        """
        获取时间表
        """