from marshmallow import post_load
from typing import Any
from core.managers.log_manager import logger

from core.managers.db_manager import db
from shared.schema.parameter_value import ParameterValueSchema
from core.model.parameter import Parameter


class ParameterValueImportSchema(ParameterValueSchema):
    @post_load
    def make_parameter_value(self, data, **kwargs):
        return ParameterValue(**data)


class ParameterValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False, default="")

    parameter_key = db.Column(db.String(), db.ForeignKey("parameter.key"))
    parameter = db.relationship("Parameter")

    def __init__(self, value, parameter):
        self.id = None
        self.value = value
        self.parameter_key = parameter

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["ParameterValue"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ParameterValue":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        pk = data.pop("parameter_key")
        logger.debug(f"pk: {pk}")
        data["parameter"] = Parameter.find_by_key(pk).to_dict()

        return data
