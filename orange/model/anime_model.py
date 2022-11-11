from orange.model.basic_model import BasicModel
from peewee import *

class Anime(BasicModel):
    # tmdb id
    id = IntegerField(primary_key=True)
    # chinese name
    name = TextField(unique=True, null=False)
    # cover url / uri
    cover = TextField()