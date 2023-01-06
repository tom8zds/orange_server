from pydantic.dataclasses import dataclass


@dataclass
class ConfigModel:
    tmdb_api_key:str
    parser:str
    source:str