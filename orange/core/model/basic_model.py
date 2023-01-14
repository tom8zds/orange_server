from typing import *
from peewee import *

db = SqliteDatabase('data.sqlite')
# _Cls = TypeVar("_Cls")

class BasicModel(Model):
    # DoesNotExist: Type[DoesNotExist]

    class Meta:
        database = db

    # @classmethod
    # def get(cls: Type[_Cls], *query: Any, **filters: Any) -> _Cls:
    #     return super().get(*query, **filters)  # type: ignore

    # @classmethod
    # def get_or_create(cls: Type[_Cls], **kwargs: Any) -> Tuple[_Cls, bool]:
    #     return super().get_or_create(**kwargs)  # type: ignoreb" database.