from typing import Any
import uuid
from sqlalchemy import or_

from core.managers.db_manager import db
from core.model.base_model import BaseModel
from core.managers.log_manager import logger


class CollectorsNode(BaseModel):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

    api_url = db.Column(db.String(), nullable=False)
    api_key = db.Column(db.String(), nullable=False)

    def __init__(self, id, name, description, api_url, api_key):
        self.id = id if id != "" else str(uuid.uuid4())
        self.name = name
        self.description = description
        self.api_url = api_url
        self.api_key = api_key

    @classmethod
    def exists_by_api_key(cls, api_key):
        return db.session.query(db.exists().where(CollectorsNode.api_key == api_key)).scalar()

    @classmethod
    def get_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(CollectorsNode.name)).all()

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            query = query.filter(
                or_(
                    CollectorsNode.name.ilike(f"%{search}%"),
                    CollectorsNode.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(CollectorsNode.name)).all(), query.count()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_first(cls):
        return cls.query.first()

    @classmethod
    def get_json_by_id(cls, id):
        return cls.get_by_id(id).to_dict()

    @classmethod
    def get_all_json(cls, search):
        nodes, count = cls.get(search)
        items = [node.to_dict() for node in nodes]
        return {"total_count": count, "items": items}

    @classmethod
    def update(cls, node_id, node_data):
        node = cls.query.get(node_id)
        node = cls.from_dict(node_data)
        db.session.commit()
        return node

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["tag"] = "mdi-animation-outline"
        data["type"] = "collector"
        return data
