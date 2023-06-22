import uuid
from marshmallow import fields, post_load
from sqlalchemy import orm, or_
from typing import Any

from core.managers.db_manager import db
from core.model.report_item import ReportItem
from core.model.user import User
from core.model.organization import Organization
from core.model.notification_template import NotificationTemplate
from shared.schema.asset import (
    AssetGroupSchema,
    AssetGroupPresentationSchema,
)
from shared.schema.user import UserIdSchema
from shared.schema.notification_template import NotificationTemplateIdSchema
from core.managers.log_manager import logger


class AssetCpe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String())

    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"))
    asset = db.relationship("Asset")

    def __init__(self, value):
        self.id = None
        self.value = value


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    serial = db.Column(db.String())
    description = db.Column(db.String())

    asset_group_id = db.Column(db.String, db.ForeignKey("asset_group.id"))
    asset_group = db.relationship("AssetGroup")

    asset_cpes = db.relationship("AssetCpe", cascade="all, delete-orphan", back_populates="asset")

    vulnerabilities = db.relationship("AssetVulnerability", cascade="all, delete-orphan", back_populates="asset")
    vulnerabilities_count = db.Column(db.Integer, default=0)

    def __init__(self, name, serial, description, asset_group_id, asset_cpes, id=None):
        self.id = id
        self.name = name
        self.serial = serial
        self.description = description
        self.asset_group_id = asset_group_id
        self.asset_cpes = asset_cpes

    @classmethod
    def get_by_cpe(cls, cpes):
        if len(cpes) <= 0:
            return []

        return (
            db.session.query(cls)
            .join(AssetCpe, cls.id == AssetCpe.asset_id)
            .filter(or_(*[AssetCpe.value.like(cpe) for cpe in cpes]))
            .distinct()
            .all()
        )

    @classmethod
    def remove_vulnerability(cls, report_item_id):
        vulnerabilities = AssetVulnerability.get_by_report(report_item_id)
        for vulnerability in vulnerabilities:
            vulnerability.asset.vulnerabilities_count -= 1
            db.session.delete(vulnerability)

    def add_vulnerability(self, report_item):
        for vulnerability in self.vulnerabilities:
            if vulnerability.report_item.id == report_item.id:
                return

        vulnerability = AssetVulnerability(self.id, report_item.id)
        db.session.add(vulnerability)
        self.vulnerabilities_count += 1

    def update_vulnerabilities(self):
        cpes = [cpe.value for cpe in self.asset_cpes]
        report_item_ids = ReportItem.get_by_cpe(cpes)

        solved = [vulnerability.report_item_id for vulnerability in self.vulnerabilities if vulnerability.solved is True]
        self.vulnerabilities = []
        self.vulnerabilities_count = 0
        for report_item_id in report_item_ids:
            vulnerability = AssetVulnerability(self.id, report_item_id)
            if report_item_id in solved:
                vulnerability.solved = True
            else:
                self.vulnerabilities_count += 1
            self.vulnerabilities.append(vulnerability)

    @classmethod
    def solve_vulnerability(cls, user, asset_id, report_item_id, solved):
        asset = cls.query.get(asset_id)
        if AssetGroup.access_allowed(user, asset.asset_group_id):
            for vulnerability in asset.vulnerabilities:
                if vulnerability.report_item_id == report_item_id:
                    if solved is not vulnerability.solved:
                        if solved:
                            asset.vulnerabilities_count -= 1
                        else:
                            asset.vulnerabilities_count += 1
                    vulnerability.solved = solved
                    db.session.commit()
                    return

    @classmethod
    def get_by_filter(cls, group_id, search, sort, vulnerable, organization):
        query = cls.query.filter(Asset.asset_group_id == group_id)

        if vulnerable:
            query = query.filter(Asset.vulnerabilities_count > 0)

        if search:
            query = query.join(AssetCpe, Asset.id == AssetCpe.asset_id).filter(
                or_(
                    Asset.name.ilike(f"%{search}%"),
                    Asset.description.ilike(f"%{search}%"),
                    Asset.serial.ilike(f"%{search}%"),
                    AssetCpe.value.ilike(f"%{search}%"),
                )
            )

        if organization:
            query = query.join(AssetGroup, Asset.asset_group_id == AssetGroup.id).filter(AssetGroup.organization == organization)

        if sort:
            if sort == "ALPHABETICAL":
                query = query.order_by(db.asc(Asset.name))
            else:
                query = query.order_by(db.desc(Asset.vulnerabilities_count))

        return query.all(), query.count()

    @classmethod
    def get_by_id(cls, asset_id, organization: Organization = None):
        query = cls.query.filter(Asset.id == asset_id)

        if organization:
            query = query.join(AssetGroup, Asset.asset_group_id == AssetGroup.id).filter(AssetGroup.organization == organization)

        return query.first()

    @classmethod
    def get_all_json(cls, user, filter):
        group_id = filter.get("group", AssetGroup.get_default_group().id)
        search = filter.get("search")
        sort = filter.get("sort")
        vulnerable = filter.get("vulnerable")
        organization = user.organization
        assets, count = cls.get_by_filter(group_id, search, sort, vulnerable, organization)
        items = [asset.to_dict() for asset in assets]
        return {"total_count": count, "items": items}, 200

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Asset"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Asset":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["asset_cpes"] = [asset_cpe.id for asset_cpe in self.asset_cpes]
        data["vulnerabilities"] = [vulnerability.id for vulnerability in self.vulnerabilities]
        data["tag"] = "mdi-laptop"
        return data

    @classmethod
    def get_json(cls, organization, asset_id):
        asset = cls.get_by_id(asset_id, organization)
        return (asset.to_dict(), 200) if asset else ("Asset Not Found", 404)

    @classmethod
    def add(cls, user, data) -> tuple[str, int]:
        asset = cls.from_dict(data)
        if not AssetGroup.access_allowed(user, asset.asset_group_id):
            return "Access Denied", 403

        db.session.add(asset)
        asset.update_vulnerabilities()
        db.session.commit()
        return f"Successfully Added {asset.id}", 201

    @classmethod
    def update(cls, user, asset_id, data) -> tuple[str, int]:
        asset = cls.query.get(asset_id)
        if not asset:
            return "Asset Not Found", 404

        if not AssetGroup.access_allowed(user, asset.asset_group_id):
            return "Access Denied", 403
        for key, value in data.items():
            if hasattr(asset, key) and key != "id":
                setattr(asset, key, value)
        asset.update_vulnerabilities()
        db.session.commit()
        return f"Succussfully updated {asset.id}", 201

    @classmethod
    def delete(cls, user, id):
        asset = cls.query.get(id)
        if not asset:
            return "Asset Not Found", 404

        if not AssetGroup.access_allowed(user, asset.asset_group_id):
            return "Access Denied", 403

        db.session.delete(asset)
        db.session.commit()
        return f"Successfully deleted {asset.id}", 200


class AssetVulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    solved = db.Column(db.Boolean, default=False)

    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"))
    asset = db.relationship("Asset", back_populates="vulnerabilities")

    report_item_id = db.Column(db.Integer, db.ForeignKey("report_item.id"))
    report_item = db.relationship("ReportItem")

    def __init__(self, asset_id, report_item_id):
        self.id = None
        self.asset_id = asset_id
        self.report_item_id = report_item_id

    @classmethod
    def get_by_report(cls, report_id):
        return cls.query.filter_by(report_item_id=report_id).all()


class NewAssetGroupGroupSchema(AssetGroupSchema):
    users = fields.Nested(UserIdSchema, many=True)
    templates = fields.Nested(NotificationTemplateIdSchema, many=True)

    @post_load
    def make(self, data, **kwargs):
        return AssetGroup(**data)


class AssetGroup(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    templates = db.relationship("NotificationTemplate", secondary="asset_group_notification_template")
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    organization = db.relationship("Organization")

    def __init__(self, id, name: str, description: str, organization_id: int, templates: list | None = None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        try:
            self.organization = Organization.find(organization_id)
            self.templates = [NotificationTemplate.find(template.id) for template in templates] if templates else []
            self.tag = "mdi-folder-multiple"
        except Exception:
            logger.exception("Error creating asset group")

    @orm.reconstructor
    def reconstruct(self):
        self.tag = "mdi-folder-multiple"

    @classmethod
    def find(cls, group_id):
        return cls.query.get(group_id)

    @classmethod
    def access_allowed(cls, user: User, group_id: str):
        return cls.query.get(group_id).organization == user.organization

    @classmethod
    def get_default_group(cls):
        return cls.query.get("default")

    @classmethod
    def get(cls, search: str | None, organization: Organization | None = None):
        query = cls.query

        if organization:
            query = query.filter_by(organization_id=organization.id)

        if search:
            query = query.filter(
                or_(
                    AssetGroup.name.ilike(f"%{search}%"),
                    AssetGroup.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(AssetGroup.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, user, search):
        groups, count = cls.get(search, user.organization)
        group_schema = AssetGroupPresentationSchema(many=True)
        return {"total_count": count, "items": group_schema.dump(groups)}

    @classmethod
    def create(cls, name: str, description: str, organization_id: int, templates: list | None = None, id: str | None = None):
        group = AssetGroup(id, name, description, organization_id, templates)
        db.session.add(group)
        db.session.commit()

    @classmethod
    def add(cls, user, data):
        group = NewAssetGroupGroupSchema().load(data)
        if not group:
            return "Invalid group data", 400
        group.organization = user.organization
        db.session.add(group)
        db.session.commit()
        return "Group added", 200

    @classmethod
    def delete(cls, user, group_id):
        if group_id == "default":
            return "Cannot delete default group", 400
        if not cls.access_allowed(user, group_id):
            return "Access denied", 403

        group = cls.query.get(group_id)
        db.session.delete(group)
        db.session.commit()

        return "Group deleted", 200

    @classmethod
    def update(cls, user, group_id, data):
        if not cls.access_allowed(user, group_id):
            return "Access denied", 403

        updated_group = NewAssetGroupGroupSchema().load(data)
        if not updated_group:
            return "Invalid group data", 400
        group = cls.query.get(group_id)
        group.name = updated_group.name
        group.description = updated_group.description
        group.templates = [added_template for added_template in updated_group.templates if added_template.organization == group.organization]
        db.session.commit()
        return "Group updated", 200


class AssetGroupNotificationTemplate(db.Model):
    asset_group_id = db.Column(db.String, db.ForeignKey("asset_group.id"), primary_key=True)
    notification_template_id = db.Column(db.Integer, db.ForeignKey("notification_template.id"), primary_key=True)
