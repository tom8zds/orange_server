from typing import List
import abc

from orange.core.subscribe.subscribe_schema import Episode

from . import schemas, dao
from orange.core.database.database import session

class Downloader(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def test_connction() -> bool:
        """
        test connnection
        """

    def _create_download(download: schemas.DownloadBase):
        return dao.create_download(session, download)
        
    def set_download_dir(dir: str) -> bool:
        """
        set download dir
        """

    @staticmethod
    @abc.abstractmethod
    def add_link(link: str, episode: Episode) -> List[schemas.Download]:
        """
        add direct link download
        return download gid
        """
    @staticmethod
    @abc.abstractmethod
    def add_metalink(link: str, episode: Episode) -> List[schemas.Download]:
        """
        add torrent link, then download by torrent file
        return torrent mission gid
        """
    @staticmethod
    @abc.abstractmethod
    def add_magnet(link: str) -> List[schemas.Download]:
        """
        add magnet download
        retuen mission gid
        """
    @staticmethod
    @abc.abstractmethod
    def get_download(gid: str) -> schemas.DownloadInfo:
        """
        return download info by gid
        """
    @staticmethod
    @abc.abstractmethod
    def get_downloads(gids: List[str]) -> List[schemas.DownloadInfo]:
        """
        return downloads info by gids
        """
