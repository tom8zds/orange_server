from pydantic import BaseModel

class DownloadBase(BaseModel):
    anime_id: int
    episode_id: int
    link: str
    mission_id: str
    status: int

class DownloadInfo(DownloadBase):
    progress: int
    total: int
    speed: int
    remain_time: int

class Download(DownloadBase):
    id: int

    class Config:
        orm_mode = True

