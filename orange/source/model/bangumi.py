from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Bangumi:
    id: int
    name: str
    cover: str

    @staticmethod
    def from_dict(obj: Any) -> 'Bangumi':
        _id = int(obj.get("id"))
        _name = str(obj.get("name"))
        _cover = str(obj.get("cover"))
        return Bangumi(_id, _name, _cover)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
