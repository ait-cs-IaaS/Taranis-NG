from sqlalchemy import func, or_

from core.managers.db_manager import db
from typing import Any


class Permission(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

    roles = db.relationship("Role", secondary="role_permission")

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def find(cls, permission_id):
        return cls.query.get(permission_id)

    @classmethod
    def add(cls, id, name, description) -> str:
        if permission := cls.find(id):
            return f"{permission.name} already exists."
        permission = cls(id=id, name=name, description=description)
        db.session.add(permission)
        db.session.commit()
        return f"Successfully created {permission.id}"

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(Permission.id)).all()

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            query = query.filter(
                or_(
                    Permission.name.ilike(f"%{search}%"),
                    Permission.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(Permission.id)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        permissions, count = cls.get(search)
        items = [permission.to_dict() for permission in permissions]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Permission"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Permission":
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def get_external_permissions_ids():
        return ["MY_ASSETS_ACCESS", "MY_ASSETS_CREATE", "MY_ASSETS_CONFIG"]

    @classmethod
    def get_external_permissions(cls):
        return [cls.find(permission_id) for permission_id in cls.get_external_permissions_ids()]

    @classmethod
    def get_external_permissions_json(cls):
        permissions = cls.get_external_permissions()
        items = [permission.to_dict() for permission in permissions]
        return {"total_count": len(items), "items": items}
