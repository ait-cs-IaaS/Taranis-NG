from marshmallow import post_load
import uuid
from sqlalchemy import or_, func
from typing import Any

from core.managers.db_manager import db
from core.model.parameter import Parameter
from shared.schema.presenter import PresenterSchema


class NewPresenterSchema(PresenterSchema):
    @post_load
    def make(self, data, **kwargs):
        return Presenter(**data)


class Presenter(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    type = db.Column(db.String(), nullable=False)

    parameters = db.relationship("Parameter", secondary="presenter_parameter")

    node_id = db.Column(db.String, db.ForeignKey("presenters_node.id"))
    node = db.relationship("PresentersNode", back_populates="presenters")

    product_types = db.relationship("ProductType", back_populates="presenter")

    def __init__(self, name, description, type, parameters):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.type = type
        self.parameters = parameters

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            search_string = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Presenter.name).like(search_string),
                    func.lower(Presenter.description).like(search_string),
                )
            )

        return query.order_by(db.asc(Presenter.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        presenters, count = cls.get(search)
        items = [presenter.to_dict() for presenter in presenters]
        return {"total_count": count, "items": items}

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def load_multiple(cls, data: list[dict[str, Any]]) -> list["Presenter"]:
        return [cls.from_dict(publisher_data) for publisher_data in data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Presenter":
        parameters = [Parameter.find_by_key(param_id) for param_id in data.pop("parameters", [])]
        return cls(parameters=parameters, **data)

    @classmethod
    def create_all(cls, presenters_data):
        new_presenter_schema = NewPresenterSchema(many=True)
        return new_presenter_schema.load(presenters_data)

    @classmethod
    def add(cls, data) -> tuple[str, int]:
        if cls.find_by_type(data["type"]):
            return "Presenter type already exists", 400

        presenter = cls.from_dict(data)

        db.session.add(presenter)
        db.session.commit()
        return f"Updated presenter {presenter.id}", 200

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_type(cls, type):
        return cls.query.filter_by(type=type).first()


class PresenterParameter(db.Model):
    presenter_id = db.Column(db.String, db.ForeignKey("presenter.id"), primary_key=True)
    parameter_key = db.Column(db.String, db.ForeignKey("parameter.key"), primary_key=True)
