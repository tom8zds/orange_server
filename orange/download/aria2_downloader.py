# external download tool connector
# watch status of mission
# on start / on finish / on fail
from typing import List
from orange.core.downloader.downloader import Downloader
import aria2p

from orange.core.downloader import schemas, dao
from orange.core.subscribe.subscribe_schema import Episode


class AriaDownloader(Downloader):

    api: aria2p.API
    download_dir: str = None

    def __init__(self, host: str, port: int, token: str = "", use_https: bool = False) -> None:
        super().__init__()

        if (use_https):
            f_host = "https://" + host
        else:
            f_host = "http://" + host

        self.api = aria2p.API(
            aria2p.Client(
                host=f_host,
                port=port,
                secret=token
            )
        )

    def set_download_dir(self, dir: str) -> bool:
        self.download_dir = dir

    def test_connction(self) -> bool:
        try:
            self.api.get_stats()
            return True
        except:
            return False

    def add_link(self, link: str,  episode: Episode) -> List[schemas.Download]:
        if (self.download_dir is not None):
            rpc_results = self.api.add(
                uri=link, options={"dir": self.download_dir})
        else:
            rpc_results = self.api.add(link)

        result = []

        for mission in rpc_results:
            download_base = schemas.DownloadBase(
            anime_id=episode.subscribe_id, episode_id=episode.id, link=link, status=0, mission_id=mission.gid)
            download = self._create_download(download_base)
            result.append(download)

        return result

    def add_metalink(self, link: str, episode: Episode) -> List[schemas.Download]:
        rpc_results: List[aria2p.Download] = []
        if (self.download_dir is not None):
            rpc_results = self.api.add_metalink(
                uri=link, options={"dir": self.download_dir})
        else:
            rpc_results = self.api.add_metalink(link)

        result = []

        download_base = schemas.DownloadBase(
            anime_id=episode.subscribe_id, episode_id=episode.id, link=link)

        for mission in rpc_results:
            download_base.status = 0
            download_base.mission_id = mission.gid
            download = self._create_download(download_base)
            result.append(download)

        return result

    def add_magnet(self, link: str) -> List[schemas.Download]:
        if (self.download_dir):
            results = self.api.add_magnet(
                uri=link, options={"dir": self.download_dir})
        else:
            results = self.api.add_magnet(link)

    def get_download(gid: str) -> schemas.DownloadInfo:
        """
        return download info by gid
        """

    def get_downloads(gids: List[str]) -> List[schemas.DownloadInfo]:
        """
        return downloads info by gids
        """
