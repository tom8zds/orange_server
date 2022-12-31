from peewee import *

from orange.model.basic_model import BasicModel

class Anime(BasicModel):
    # db id
    id = IntegerField(primary_key=True)
    # chinese name
    name = TextField(unique=True, null=False)
    # cover url / uri start with http(s)://
    cover = TextField()
    # description
    overview = TextField()