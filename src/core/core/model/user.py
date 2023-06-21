from marshmallow import fields, post_load
from sqlalchemy import or_, orm
from werkzeug.security import generate_password_hash
from typing import Any

from core.managers.db_manager import db
from core.model.role import Role
from core.model.permission import Permission
from core.model.organization import Organization
from shared.schema.user import (
    UserSchemaBase,
    UserProfileSchema,
    HotkeySchema,
)

from shared.schema.role import RoleIdSchema, PermissionIdSchema
from shared.schema.organization import OrganizationSchema
from core.managers.log_manager import logger


class NewUserSchema(UserSchemaBase):
    password = fields.Str(required=False)
    roles = fields.Nested(RoleIdSchema, many=True, only=["id"])
    permissions = fields.Nested(PermissionIdSchema, many=True)
    organization = fields.Nested(OrganizationSchema, only=["id"])

    @post_load
    def make(self, data, **kwargs):
        return User(**data)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=True)

    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    organization = db.relationship("Organization")

    roles = db.relationship(Role, secondary="user_role")
    permissions = db.relationship(Permission, secondary="user_permission")

    profile_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"))
    profile = db.relationship("UserProfile", cascade="all")

    def __init__(self, username, name, password, organization, roles, permissions, id=None):
        self.id = id
        self.username = username
        self.name = name
        self.password = generate_password_hash(password)
        self.organization = Organization.find(organization["id"]) if isinstance(organization, dict) else Organization.find(organization)
        self.roles = [Role.find(role["id"]) for role in roles]
        self.permissions = [Permission.find(permission["id"]) for permission in permissions]
        self.profile = UserProfile(True, False, [], "en")

    @classmethod
    def find(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def find_by_role(cls, role_id: int):
        return cls.query.join(Role, Role.id == role_id).all()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(User.name)).all()

    @classmethod
    def get(cls, search, organization):
        query = cls.query

        if organization:
            query = query.filter(User.organization_id == organization.id)

        if search is not None:
            query = query.filter(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(User.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search=None):
        users, count = cls.get(search, None)
        items = [user.to_dict() for user in users]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Role"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Role":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password"}
        data["roles"] = [role.id for role in self.roles]
        data["permissions"] = [permission.id for permission in self.permissions]
        data["tag"] = "mdi-account"
        return data

    @classmethod
    def add_new(cls, data) -> tuple[str, int]:
        user = cls.from_dict(data)
        db.session.add(user)
        db.session.commit()
        return f"User {user.id} created", 201

    @classmethod
    def update(cls, user_id, data) -> tuple[str, int]:
        user = cls.query.get(user_id)
        if user is None:
            return f"User {user_id} not found", 404
        updated_user = cls.from_dict(data)
        for key, value in vars(updated_user).items():
            if hasattr(user, key) and key != "id":
                setattr(user, key, value)

        db.session.commit()
        return f"User {user_id} updated", 200

    def get_permissions(self):
        all_permissions = {permission.id for permission in self.permissions}

        for role in self.roles:
            all_permissions.update(role.get_permissions())
        return list(all_permissions)

    def get_current_organization_name(self):
        return self.organization.name if self.organization else ""

    @classmethod
    def get_profile_json(cls, user):
        return UserProfileSchema().dump(user.profile)

    @classmethod
    def update_profile(cls, user, data):
        user.profile = NewUserProfileSchema().load(data)
        db.session.commit()
        return cls.get_profile_json(user)

    @classmethod
    def delete(cls, id):
        user = cls.query.get(id)
        db.session.delete(user)
        db.session.commit()

    ##
    # External User Management - TODO: Check if this is still needed
    ##

    @classmethod
    def get_all_external_json(cls, user, search):
        users, count = cls.get(search, user.organization)
        items = [user.to_dict() for user in users]
        return {"total_count": count, "items": items}

    @classmethod
    def add_new_external(cls, user, data):
        permissions = Permission.get_external_permissions_ids()
        data.pop("roles")
        for permission in data["permissions"]:
            if permission["id"] not in permissions:
                data["permissions"].remove(permission)
        user = cls.from_dict(data)
        db.session.add(user)
        db.session.commit()
        return f"User {user.id} created", 201

    @classmethod
    def update_external(cls, user, user_id, data):
        permissions = Permission.get_external_permissions_ids()
        user = cls.query.get(user_id)
        if user is None:
            return f"User {user_id} not found", 404

        updated_user = cls.from_dict(data)
        if user.organization != updated_user.organization:
            return f"User {user_id} could not be updated", 400
        user.username = updated_user.username
        user.name = updated_user.name

        for permission in updated_user.permissions:
            if permission.id not in permissions:
                updated_user.permissions.remove(permission)

        user.permissions = updated_user.permissions

        db.session.commit()
        return f"User {user_id} updated", 200

    @classmethod
    def delete_external(cls, user, id):
        existing_user = cls.query.get(id)
        if user.organization != existing_user.organization:
            return f"User {id} could not be deleted", 400
        db.session.delete(existing_user)
        db.session.commit()
        return f"User {id} deleted", 200


class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)


class UserPermission(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    permission_id = db.Column(db.String, db.ForeignKey("permission.id"), primary_key=True)


class NewHotkeySchema(HotkeySchema):
    @post_load
    def make(self, data, **kwargs):
        return Hotkey(**data)


class NewUserProfileSchema(UserProfileSchema):
    hotkeys = fields.List(fields.Nested(NewHotkeySchema))

    @post_load
    def make(self, data, **kwargs):
        return UserProfile(**data)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    spellcheck = db.Column(db.Boolean, default=True)
    dark_theme = db.Column(db.Boolean, default=False)

    hotkeys = db.relationship("Hotkey", cascade="all, delete-orphan")
    language = db.Column(db.String(2), default="en")

    def __init__(self, spellcheck, dark_theme, hotkeys, language="en"):
        self.id = None
        self.spellcheck = spellcheck
        self.dark_theme = dark_theme
        self.hotkeys = hotkeys
        self.language = language


class Hotkey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_code = db.Column(db.Integer)
    key = db.Column(db.String)
    alias = db.Column(db.String)

    user_profile_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"))

    def __init__(self, key_code, key, alias):
        self.id = None
        self.key_code = key_code
        self.key = key
        self.alias = alias
