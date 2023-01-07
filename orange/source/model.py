from pydantic.dataclasses import dataclass
from enum import Enum, IntEnum
from typing import List


@dataclass
class Bangumi:
    id: int
    name: str
    cover: str


@dataclass
class SubscribeItem:
    link: str
    title: str
    description: str
    torrent: str
    size: int
    update: float


@dataclass
class SubscribeChannel:
    title: str
    link: str
    description: str
    items: List[SubscribeItem]


@dataclass
class SubGroup:
    id: int
    name: str


@dataclass
class BangumiDetail:
    info: Bangumi
    subGroups: List[SubGroup]


class Season(IntEnum):
    SPRING = 4
    SUMMER = 7
    AUTUMN = 10
    WINTER = 1
    OTHER = 0


class WeekDay(IntEnum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7
    OTH = 0


SeasonData = {
    Season.SPRING: {
        "ch": "四月"
    },
    Season.SUMMER: {
        "ch": "七月"
    },
    Season.AUTUMN: {
        "ch": "十月"
    },
    Season.WINTER: {
        "ch": "一月"
    },
    Season.OTHER: {
        "ch": "其他"
    }
}

# 时间点, 用于切换年份和季度
@dataclass
class TimeTable:
    year: int
    season: Season
    table: dict[str, List[Bangumi]]
