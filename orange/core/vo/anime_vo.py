from pydantic.dataclasses import dataclass


@dataclass
class AnimeVO():
    # db id
    id:str
    # db season id
    season_id:str
    # chinese name
    name:str
    # season name
    season_name:str
    # cover url / uri start with http(s)://
    cover:str
    # description
    overview:str