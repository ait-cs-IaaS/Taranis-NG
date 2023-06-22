from sqlalchemy import func, or_, orm
from typing import Any

from core.managers.db_manager import db
from core.model.address import Address
from core.managers.log_manager import logger


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    address = db.relationship("Address", cascade="all")

    def __init__(self, name, description, address, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.address = address
        self.tag = "mdi-office-building"

    @orm.reconstructor
    def reconstruct(self):
        self.tag = "mdi-office-building"

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["address"] = self.address.to_dict() if self.address else None
        data.pop("address_id")
        return data

    @classmethod
    def find(cls, organization_id):
        return cls.query.get(organization_id)

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(Organization.name)).all()

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            query = query.filter(
                or_(
                    Organization.name.ilike(f"%{search}%"),
                    Organization.description.ilike(f"%{search}%"),
                )
            )

        return query.order_by(db.asc(Organization.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        organizations, count = cls.get(search)
        items = [organization.to_dict() for organization in organizations]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Organization"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Organization":
        address_data = data.pop("address", None)
        address = Address.from_dict(address_data) if address_data else None
        return cls(address=address, **data)

    @classmethod
    def add_new(cls, data):
        address = Address.from_dict(data.pop("address"))
        organization = cls.from_dict(data)
        organization.address = address
        db.session.add(organization)
        db.session.commit()

    @classmethod
    def update(cls, organization_id, data) -> tuple[str, int]:
        organization = cls.query.get(organization_id)
        if organization is None:
            return f"Organization with id {organization_id} not found", 404

        if address_data := data.pop("address", None):
            address_update_message, status_code = organization.address.update(address_data)
            if status_code != 200:
                return address_update_message, status_code

        for key, value in data.items():
            if hasattr(organization, key) and key != "id":
                setattr(organization, key, value)

        db.session.commit()
        return f"Successfully updated {organization.id}", 200

    @classmethod
    def delete(cls, id):
        organization = cls.query.get(id)
        db.session.delete(organization)
        db.session.commit()
