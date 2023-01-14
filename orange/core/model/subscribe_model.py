from orange.core.model.basic_model import BasicModel, db
from peewee import *

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

db.create_tables([Subscribe])

        
