from sqlalchemy import or_
import uuid
from typing import Any
from enum import StrEnum, auto

from core.managers.db_manager import db
from core.model.parameter_value import ParameterValue
from core.model.base_model import BaseModel


class COLLECTOR_TYPES(StrEnum):
    RSS_COLLECTOR = auto()
    EMAIL_COLLECTOR = auto()
    TWITTER_COLLECTOR = auto()
    WEB_COLLECTOR = auto()
    MANUAL_COLLECTOR = auto()


class BOT_TYPES(StrEnum):
    ANALYST_BOT = auto()
    GROUPING_BOT = auto()
    NLP_BOT = auto()
    TAGGING_BOT = auto()
    STORY_BOT = auto()
    SUMMARY_BOT = auto()
    WORDLIST_BOT = auto()


class PRESENTER_TYPES(StrEnum):
    PDF_PRESENTER = auto()
    HTML_PRESENTER = auto()
    TEXT_PRESENTER = auto()
    MISP_PRESENTER = auto()


class PUBLISHER_TYPES(StrEnum):
    FTP_PUBLISHER = auto()
    EMAIL_PUBLISHER = auto()
    TWITTER_PUBLISHER = auto()
    WORDPRESS_PUBLISHER = auto()
    MISP_PUBLISHER = auto()


class WORKER_TYPES(StrEnum):
    RSS_COLLECTOR = auto()
    EMAIL_COLLECTOR = auto()
    TWITTER_COLLECTOR = auto()
    WEB_COLLECTOR = auto()
    MANUAL_COLLECTOR = auto()
    ANALYST_BOT = auto()
    GROUPING_BOT = auto()
    NLP_BOT = auto()
    TAGGING_BOT = auto()
    STORY_BOT = auto()
    SUMMARY_BOT = auto()
    WORDLIST_BOT = auto()
    PDF_PRESENTER = auto()
    HTML_PRESENTER = auto()
    TEXT_PRESENTER = auto()
    MISP_PRESENTER = auto()
    FTP_PUBLISHER = auto()
    EMAIL_PUBLISHER = auto()
    TWITTER_PUBLISHER = auto()
    WORDPRESS_PUBLISHER = auto()
    MISP_PUBLISHER = auto()


class WORKER_CATEGORY(StrEnum):
    COLLECTOR = auto()
    BOT = auto()
    PRESENTER = auto()
    PUBLISHER = auto()


class Worker(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    type = db.Column(db.Enum(WORKER_TYPES), nullable=False)
    category = db.Column(db.Enum(WORKER_CATEGORY), nullable=False)
    parameters = db.relationship("ParameterValue", secondary="worker_parameter_value", cascade="all")

    def __init__(self, name, description, type, parameters):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.type = type
        self.category = self.type.split("_")[1]
        self.parameters = parameters

    @classmethod
    def add(cls, data) -> tuple[dict[str, str], int]:
        if cls.filter_by_type(data["type"]):
            return {"error": f"Worker with type {data['type']} already exists"}, 409
        worker = cls.from_dict(data)
        db.session.add(worker)
        db.session.commit()
        return {"message": f"Worker {worker.name} added", "id": worker.id}, 201

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def get_type(cls, id) -> "Worker":
        if worker := cls.get(id):
            return worker.type
        else:
            raise ValueError

    @classmethod
    def get_by_filter(cls, filter_args):
        query = cls.query

        if search := filter_args.get("search"):
            query = query.filter(
                or_(
                    Worker.name.ilike(f"%{search}%"),
                    Worker.description.ilike(f"%{search}%"),
                )
            )

        if category := filter_args.get("category"):
            query = query.filter(Worker.category == category)

        if type := filter_args.get("type"):
            query = query.filter(Worker.type == type)

        return query.order_by(db.asc(Worker.name)).all(), query.count()

    @classmethod
    def filter_by_type(cls, type):
        return cls.query.filter_by(type=type).first()

    @classmethod
    def get_all_json(cls, filter_args):
        workers, count = cls.get_by_filter(filter_args)
        items = [worker.to_worker_info_dict() for worker in workers]
        return {"total_count": count, "items": items}

    def to_worker_info_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "parameters": {parameter.parameter.key: parameter.value for parameter in self.parameters},
        }

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["parameters"] = [pv.to_dict() for pv in self.parameters]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Worker":
        if parameters := data.pop("parameters", None):
            data["parameters"] = ParameterValue.from_parameter_list(parameters)

        return cls(**data)


class WorkerParameterValue(BaseModel):
    worker_id = db.Column(db.String, db.ForeignKey("worker.id", ondelete="CASCADE"), primary_key=True)
    parameter_value_id = db.Column(db.Integer, db.ForeignKey("parameter_value.id"), primary_key=True)
