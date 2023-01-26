from enum import IntEnum
from peewee import *

class SubscribeStatus(IntEnum):
    ongoing: 0
    finish: 1

class SubscribeQuality(IntEnum):
    720: 0
    1080: 1
    any: 2

class SubscribeLang(IntEnum):
    RAW: 0
    SC: 1
    TC: 2


class Subscribe:
    id:AutoField()
    source:TextField()
    source_id:TextField()
    rss:TextField()
    quality:IntegerField()
    language:IntegerField()
    filter:TextField()


class Anime:
    # db id
    id = IntegerField(primary_key=True)
    # chinese name
    name = TextField(null=False)
    # cover url / uri start with http(s)://
    cover = TextField(null=False)
    # description
    overview = TextField()


class Season:
    id:IntegerField(primary_key=True)
    anime:ForeignKeyField(Anime, backref='seasons')
    name:TextField()
    order:IntegerField()
    # status, if finish, not loading on refresh
    status:IntegerField()

class EpisodeStatus(IntEnum):
    notDownload:0
    downloading:1
    downloaded:2


class Episode:
    id:IntegerField(primary_key=True)
    season:ForeignKeyField(Season, backref='episodes')
    name:TextField()
    status:IntegerField()

class DownloadStatus(IntEnum):
    downloading: 0
    pause: 1
    seeding: 2
    end: 3


class DownloadQueue:
    id:IntegerField(primary_key=True)
    Episode:ForeignKeyField(Episode, backref='downloads')
    status:IntegerField()