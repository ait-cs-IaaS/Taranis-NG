from sqlalchemy import func, or_, orm, and_
from marshmallow import fields, post_load
from flask_sqlalchemy import query
from typing import Any

from core.managers.db_manager import db
from core.model.role import Role
from core.model.user import User
from shared.schema.role import RoleIdSchema
from shared.schema.user import UserIdSchema
from shared.schema.acl_entry import ACLEntrySchema, ACLEntryPresentationSchema, ItemType


class NewACLEntrySchema(ACLEntrySchema):
    users = fields.Nested(UserIdSchema, many=True)
    roles = fields.Nested(RoleIdSchema, many=True)

    @post_load
    def make(self, data, **kwargs):
        return ACLEntry(**data)


class ACLEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String())

    item_type = db.Column(db.Enum(ItemType))
    item_id = db.Column(db.String(64))

    everyone = db.Column(db.Boolean, default=True)
    users = db.relationship("User", secondary="acl_entry_user")
    roles = db.relationship("Role", secondary="acl_entry_role")

    see = db.Column(db.Boolean)
    access = db.Column(db.Boolean)
    modify = db.Column(db.Boolean)

    def __init__(self, name, description, item_type, item_id, everyone, users, see, access, modify, roles, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.item_type = item_type
        self.item_id = item_id
        self.everyone = everyone
        self.see = see
        self.access = access
        self.modify = modify
        self.users = [User.find_by_id(user.id) for user in users]
        self.roles = [Role.find(role.id) for role in roles]
        self.tag = "mdi-lock-check"

    @orm.reconstructor
    def reconstruct(self):
        self.tag = "mdi-lock-check"

    @classmethod
    def find(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(ACLEntry.name)).all()

    @classmethod
    def has_rows(cls) -> bool:
        return cls.query.count() > 0

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            query = query.filter(
                or_(
                    ACLEntry.name.ilike(f"%{search}%"),
                    ACLEntry.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(ACLEntry.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        acls, count = cls.get(search)
        items = [acl.to_dict() for acl in acls]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["ACLEntry"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ACLEntry":
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def add_new(cls, data):
        acl = cls.from_dict(data)
        db.session.add(acl)
        db.session.commit()
        return f"Successfully Added {acl.id}", 201

    @classmethod
    def update(cls, acl_id, data):
        schema = NewACLEntrySchema()
        updated_acl = schema.load(data)
        if not updated_acl:
            return
        acl = cls.query.get(acl_id)
        for key in vars(updated_acl):
            setattr(acl, key, getattr(updated_acl, key))
        db.session.commit()

    @classmethod
    def delete(cls, id):
        acl = cls.query.get(id)
        db.session.delete(acl)
        db.session.commit()

    @classmethod
    def apply_query(cls, query: query.Query, user: User, see: bool, access: bool, modify: bool) -> query.Query:
        roles = [role.id for role in user.roles]

        query = query.outerjoin(
            ACLEntryUser,
            and_(
                ACLEntryUser.acl_entry_id == ACLEntry.id,
                ACLEntryUser.user_id == user.id,
            ),
        )

        query = query.outerjoin(ACLEntryRole, ACLEntryRole.acl_entry_id == ACLEntry.id)

        if see:
            return query.filter(
                or_(
                    ACLEntry.id is not None,
                    and_(
                        ACLEntry.see is True,
                        or_(
                            ACLEntry.everyone is True,
                            ACLEntryUser.user_id == user.id,
                            ACLEntryRole.role_id.in_(roles),
                        ),
                    ),
                )
            )

        if access:
            return query.filter(
                or_(
                    ACLEntry.id is not None,
                    and_(
                        ACLEntry.access is True,
                        or_(
                            ACLEntry.everyone is True,
                            ACLEntryUser.user_id == user.id,
                            ACLEntryRole.role_id.in_(roles),
                        ),
                    ),
                )
            )

        if modify:
            return query.filter(
                or_(
                    ACLEntry.id is not None,
                    and_(
                        ACLEntry.modify is True,
                        or_(
                            ACLEntry.everyone is True,
                            ACLEntryUser.user_id == user.id,
                            ACLEntryRole.role_id.in_(roles),
                        ),
                    ),
                )
            )

        return query.filter(
            or_(
                ACLEntry.id is not None,
                ACLEntry.everyone is True,
                ACLEntryUser.user_id == user.id,
                ACLEntryRole.role_id.in_(roles),
            )
        )


class ACLEntryUser(db.Model):
    acl_entry_id = db.Column(db.Integer, db.ForeignKey("acl_entry.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)


class ACLEntryRole(db.Model):
    acl_entry_id = db.Column(db.Integer, db.ForeignKey("acl_entry.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)
