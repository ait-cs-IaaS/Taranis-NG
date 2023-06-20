from core.managers.db_manager import db
from typing import Any
from core.managers.log_manager import logger


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String())
    city = db.Column(db.String())
    zip = db.Column(db.String())
    country = db.Column(db.String())

    def __init__(self, street, city, zip, country, id=None):
        self.id = id
        self.street = street
        self.city = city
        self.zip = zip
        self.country = country

    @classmethod
    def find(cls, address_id):
        return cls.query.get(address_id)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Address":
        return cls(**data)

    def update(self, new_item: dict[str, Any]) -> tuple[str, int]:
        for key, value in new_item.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)

        db.session.commit()
        return f"Successfully updated {self.id}", 200

    def update_from_address(self, new_address: "Address") -> tuple[str, int]:
        return self.update(new_address.to_dict())
