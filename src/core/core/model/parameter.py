from typing import Any
from enum import Enum, auto

from core.managers.db_manager import db


class ParameterType(Enum):
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    LIST = auto()


class Parameter(db.Model):
    key = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    type = db.Column(db.Enum(ParameterType))

    def __init__(self, key, name, description, type):
        self.key = key
        self.name = name
        self.description = description
        self.type = type

    @classmethod
    def add(cls, data):
        if cls.find_by_key(data["key"]):
            return f"{data['key']} already exists."
        parameter = cls.from_dict(data)
        db.session.add(parameter)
        db.session.commit()
        return f"Successfully created {parameter.key}"

    @classmethod
    def find_by_key(cls, key):
        return cls.query.get(key)

    @classmethod
    def get_all_json(cls):
        parameters, count = cls.query.all(), cls.query.count()
        items = [parameter.to_dict() for parameter in parameters]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Parameter"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Parameter":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["type"] = self.type.name
        return data
