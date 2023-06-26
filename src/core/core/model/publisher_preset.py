from typing import Any
import uuid

from core.managers.log_manager import logger
from core.managers.db_manager import db
from core.model.base_model import BaseModel
from core.model.publishers_node import PublishersNode


class PublisherPreset(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    publisher_id = db.Column(db.String, db.ForeignKey("publisher.id"))
    publisher = db.relationship("Publisher", back_populates="presets")

    use_for_notifications = db.Column(db.Boolean)

    parameter_values = db.relationship("ParameterValue", secondary="publisher_preset_parameter_value", cascade="all")

    def __init__(
        self,
        name,
        description,
        publisher_id,
        parameter_values,
        use_for_notifications=False,
        id=None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.publisher_id = publisher_id
        self.parameter_values = parameter_values
        self.use_for_notifications = use_for_notifications

    @classmethod
    def find_for_notifications(cls):
        return cls.query.filter_by(use_for_notifications=True).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(PublisherPreset.name)).all()

    @classmethod
    def get_by_filter(cls, search=None):
        query = cls.query

        if search:
            query = query.filter(
                db.or_(
                    cls.name.ilike(f"%{search}%"),
                    cls.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(cls.name).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        publishers, count = cls.get_by_filter(search)
        items = [publisher.to_dict() for publisher in publishers]
        return {"total_count": count, "items": items}

    @classmethod
    def get_all_for_publisher_json(cls, parameters):
        node = PublishersNode.get_by_api_key(parameters.api_key)
        for publisher in node.publishers:
            if publisher.type == parameters.publisher_type:
                return [preset.to_dict() for preset in publisher.sources]

    @classmethod
    def update(cls, preset_id, data):
        preset = cls.query.get(preset_id)
        updated_preset = cls.from_dict(data)
        preset.name = updated_preset.name
        preset.description = updated_preset.description

        for value in preset.parameter_values:
            for updated_value in updated_preset.parameter_values:
                if value.parameter_key == updated_value.parameter_key:
                    value.value = updated_value.value

        db.session.commit()

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["parameter_values"] = [value.to_dict() for value in self.parameter_values]
        data["tag"] = "mdi-file-star-outline"
        return data


class PublisherPresetParameterValue(BaseModel):
    publisher_preset_id = db.Column(db.String, db.ForeignKey("publisher_preset.id"), primary_key=True)
    parameter_value_id = db.Column(db.Integer, db.ForeignKey("parameter_value.id"), primary_key=True)
