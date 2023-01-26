from enum import IntEnum
from typing import List
from pydantic.dataclasses import dataclass

qualities = {
    "2160p": 0,
    "1080p": 1,
    "720p": 2,
    "other": 3,
}

class Quality(IntEnum):
    uhd: 0
    fhd: 1
    hd: 2
    other: 3

class SubLanguage(IntEnum):
    simple:0
    traditional:1

@dataclass
class FilterOption:
    title:List[str]
    quality:Quality
    language:SubLanguage

@dataclass
class Subscribe:
    source_id:str
    db_tv_id:str
    season_number:int
    filter: FilterOption

@dataclass
class SubscribeVO():
    source_id:str
    provider_id:str
    tv_id:str
    season_number:int