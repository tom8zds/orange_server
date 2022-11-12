from enum import Enum
from dataclasses import dataclass
from typing import List

from orange.source.model.bangumi import Bangumi

class Season(Enum):
    SPRING = 4
    SUMMER = 7
    AUTUMN = 10
    WINTER = 1
    OTHER  = 0

class WeekDay(Enum):
    MON = 1
    TUE = 2
    THR = 3
    WED = 4
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
    table: dict[WeekDay, List[Bangumi]]
