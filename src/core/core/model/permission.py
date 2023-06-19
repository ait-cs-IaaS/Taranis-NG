from sqlalchemy import func, or_

from core.managers.db_manager import db
from shared.schema.role import PermissionSchema
from typing import Any


class Permission(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

    roles = db.relationship("Role", secondary="role_permission")

    @classmethod
    def find(cls, permission_id):
        return cls.query.get(permission_id)

    @classmethod
    def add(cls, id, name, description):
        permission = cls.find(id)
        if permission is None:
            permission = Permission()
            permission.id = id
            permission.name = name
            permission.description = description
            db.session.add(permission)
        else:
            permission.name = name
            permission.description = description
        db.session.commit()

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
