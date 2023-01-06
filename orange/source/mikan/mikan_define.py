from orange.source.model import Season, WeekDay


MIKAN_BASE = 'https://mikanani.me'
MIKAN_SEASON = '/Home/BangumiCoverFlowByDayOfWeek'
MIKAN_BANGUMI = '/Home/Bangumi'

MikanSeasonData = {
    Season.SPRING: {
        "ch": "春"
    },
    Season.SUMMER: {
        "ch": "夏"
    },
    Season.AUTUMN: {
        "ch": "秋"
    },
    Season.WINTER: {
        "ch": "冬"
    },
    Season.OTHER: {
        "ch": "OVA"
    }
}

MikanWeekDay = {
    '星期六': WeekDay.SAT,
    '星期日': WeekDay.SUN,
    '星期一': WeekDay.MON,
    '星期二': WeekDay.TUE,
    '星期三': WeekDay.WED,
    '星期四': WeekDay.THU,
    '星期五': WeekDay.FRI,
    '剧场版': WeekDay.OTH,
    'OVA': WeekDay.OTH,
}