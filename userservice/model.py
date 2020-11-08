from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(unsafe_hash=True)
class User:
    name: str
    email: str
    id: str = None
