from marshmallow import post_load
from typing import Any
from core.managers.log_manager import logger

from core.managers.db_manager import db
from core.model.base_model import BaseModel
from core.model.parameter import Parameter


class ParameterValue(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False, default="")

    parameter_key = db.Column(db.String(), db.ForeignKey("parameter.key"))
    parameter = db.relationship("Parameter")

    def __init__(self, value, parameter):
        self.id = None
        self.value = value
        self.parameter_key = parameter

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["parameter"] = Parameter.find_by_key(data.pop("parameter_key")).to_dict()
        return data
