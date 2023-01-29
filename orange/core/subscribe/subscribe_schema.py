from pydantic import BaseModel
from enum import IntEnum
from typing import List
from pydantic.dataclasses import dataclass

qualities = {
    0: "2160p",
    1: "1080p",
    2: "720p",
    3: "other",
}


class Quality(IntEnum):
    uhd: 0
    fhd: 1
    hd: 2
    other: 3


class SubLanguage(IntEnum):
    simple: 0
    traditional: 1


@dataclass
class ParseParam:
    name: str
    alt_names: List[str]
    unwanted: List[str]
    quality: int = 1
    language: int = 0


class EpisodeBase(BaseModel):
    anime_name: str
    season_number: int
    episode_number: int


class EpisodeParse(EpisodeBase):
    valide: bool = False
    exist: bool = False
    resolve: bool = False
    parser: str 

class EpisodeCreate(EpisodeBase):
    subscribe_id: int

class Episode(EpisodeCreate):
    id: int

    class Config:
        orm_mode = True


class SubscribeBase(BaseModel):
    tv_id: str
    status: int = 0
    source_id: str
    provider_id: str
    season_number: int


class SubscribeCreate(SubscribeBase):
    parse_param: ParseParam


class Subscribe(SubscribeBase):
    id: int
    name: str
    status: int
    season_number: int
    parse_param: str
    episodes: List[Episode]

    class Config:
        orm_mode = True
