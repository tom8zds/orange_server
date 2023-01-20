from orange.core.model.basic_model import BasicModel, db
from peewee import *

class EpisodeRecord(BasicModel):
    id= AutoField(primary_key= True)
    anime_id= CharField()
    season_number= IntegerField()
    episode_number= IntegerField()

    class Meta:
        indexes = (
            # create a unique on from/to/date
            (('anime_id', 'season_number', 'episode_number'), True),
        )

class Subscribe(BasicModel):
    id= AutoField(primary_key = True)
    name= CharField()
    status= IntegerField()
    tv_id= CharField()
    season_number= IntegerField()
    source_id= CharField()
    provider_id= CharField()
    quality= IntegerField()
    language= IntegerField()

db.create_tables([Subscribe, EpisodeRecord])

        
