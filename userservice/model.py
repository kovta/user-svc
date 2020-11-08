from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from marshmallow_dataclass import dataclass as marshmallow_dataclass
from marshmallow import fields
import marshmallow.validate


@dataclass
@dataclass_json
@marshmallow_dataclass
class User:
    email: str = field(metadata={"validate": marshmallow.validate.Email()})
    name: str = fields.String(required=True)
    id: str = fields.String(required=True)


@marshmallow_dataclass
class CreateUser:
    email: str = field(metadata={"validate": marshmallow.validate.Email()})
    name: str = fields.String(required=True)


class InvalidInputError(Exception):
    """Supplied input is invalid or inconsistent"""
