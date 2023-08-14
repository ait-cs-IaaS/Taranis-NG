from typing import Any
from core.managers.log_manager import logger

from core.managers.db_manager import db
from core.model.base_model import BaseModel


class ParameterValue(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    parameter = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False, default="")

    def __init__(self, parameter, value="", id=None):
        self.id = id
        self.parameter = parameter
        self.value = value

    def to_dict(self) -> dict[int, Any]:
        return {self.parameter: self.value}

    @classmethod
    def get_or_create(cls, data: dict[str, Any]) -> "ParameterValue":
        if "id" in data:
            return cls.get(data["id"])
        if "parameter" in data and "value" in data:
            return cls.from_dict(data)
        return cls.from_dict({"parameter": list(data.keys())[0], "value": list(data.values())[0]})

    @classmethod
    def get_or_create_from_list(cls, parameters: dict[str, Any] | list[str] | list[dict[str, Any]]) -> list["ParameterValue"]:
        if parameters and isinstance(parameters, list):
            if isinstance(parameters[0], dict):
                return [cls.get_or_create(parameter) for parameter in parameters]  # type: ignore
            return cls.from_parameter_list(parameters)  # type: ignore
        return [cls.get_or_create({"parameter": key, "value": val}) for key, val in parameters.items()]  # type: ignore

    @classmethod
    def from_parameter_list(cls, parameters: list[str]) -> list["ParameterValue"]:
        return [cls(parameter=parameter) for parameter in parameters]
