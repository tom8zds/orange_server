from dataclasses import dataclass


@dataclass
class AnimeVO():
    # db id
    id:str
    # chinese name
    name:str
    # cover url / uri start with http(s)://
    cover:str
    # description
    overview:str