import os
from xml.etree.ElementTree import iterparse
from marshmallow import fields, post_load
from sqlalchemy import func, or_
from enum import Enum, auto
from typing import Any

from core.managers.log_manager import logger
from core.managers.db_manager import db


class AttributeType(Enum):
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    RADIO = auto()
    ENUM = auto()
    TEXT = auto()
    RICH_TEXT = auto()
    DATE = auto()
    TIME = auto()
    DATE_TIME = auto()
    LINK = auto()
    ATTACHMENT = auto()
    TLP = auto()
    CPE = auto()
    CVE = auto()
    CVSS = auto()


class AttributeValidator(Enum):
    NONE = auto()
    EMAIL = auto()
    NUMBER = auto()
    RANGE = auto()
    REGEXP = auto()


class AttributeEnum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    value = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    imported = db.Column(db.Boolean, default=False)

    attribute_id = db.Column(db.Integer, db.ForeignKey("attribute.id", ondelete="CASCADE"))
    attribute = db.relationship("Attribute", cascade="all, delete")

    def __init__(self, index, value, description, id=None):
        self.id = id
        self.index = index
        self.value = value
        self.description = description

    @classmethod
    def count_for_attribute(cls, attribute_id) -> int:
        return cls.query.filter_by(attribute_id=attribute_id).count()

    @classmethod
    def get_all_for_attribute(cls, attribute_id):
        return cls.query.filter_by(attribute_id=attribute_id).order_by(db.asc(cls.index)).all()

    @classmethod
    def get_for_attribute(cls, attribute_id, search, offset, limit):
        query = cls.query.filter_by(attribute_id=attribute_id)
        if search:
            search_string = f"%{search}%"
            query = query.filter(
                or_(
                    AttributeEnum.value.ilike(search_string),
                    AttributeEnum.description.ilike(search_string),
                )
            )

        query = query.order_by(db.asc(AttributeEnum.index))

        return query.offset(offset).limit(limit).all(), query.count()

    @classmethod
    def find_by_value(cls, attribute_id, value):
        return cls.query.filter_by(attribute_id=attribute_id).filter(func.lower(AttributeEnum.value) == value.lower()).first()

    @classmethod
    def get_for_attribute_json(cls, attribute_id, search, offset, limit):
        attribute_enums, total_count = cls.get_for_attribute(attribute_id, search, offset, limit)
        items = [attribute_enum.to_dict() for attribute_enum in attribute_enums]
        return {
            "total_count": total_count,
            "items": items,
        }

    @classmethod
    def delete_for_attribute(cls, attribute_id):
        cls.query.filter_by(attribute_id=attribute_id).delete()
        db.session.commit()

    @classmethod
    def delete_imported_for_attribute(cls, attribute_id):
        cls.query.filter_by(attribute_id=attribute_id, imported=True).delete()
        db.session.commit()

    @classmethod
    def add(cls, attribute_id, data) -> tuple[str, int]:
        count = cls.count_for_attribute(attribute_id) + 1
        attribute_enum = cls.from_dict(data["items"])
        attribute_enum.index = count
        db.session.add(attribute_enum)
        db.session.commit()
        return f"Added {attribute_enum.value}", 201

    @classmethod
    def update(cls, enum_id, data) -> tuple[str, int]:
        attribute_enum = cls.query.get(enum_id)
        if not attribute_enum:
            return "Attribute Enum not found", 404
        for key, value in data.items():
            if hasattr(attribute_enum, key) and key != "id":
                setattr(attribute_enum, key, value)
        db.session.commit()
        return f"Attribute Enum {attribute_enum.id} updated", 200

    @classmethod
    def delete(cls, attribute_enum_id) -> tuple[str, int]:
        cls.query.get(attribute_enum_id).delete()
        db.session.commit()
        return f"Attribute Enum {attribute_enum_id} deleted", 200

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["AttributeEnum"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AttributeEnum":
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Attribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    type = db.Column(db.Enum(AttributeType))
    default_value = db.Column(db.String())

    validator = db.Column(db.Enum(AttributeValidator))
    validator_parameter = db.Column(db.String())

    def __init__(self, name, description, type, default_value, validator, validator_parameter, attribute_enums, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.default_value = default_value
        self.validator = validator
        self.validator_parameter = validator_parameter
        self.attribute_enums = attribute_enums

    @classmethod
    def get_all(cls):
        return cls.query.order_by(Attribute.name).all()

    @classmethod
    def find_by_type(cls, attribute_type):
        return cls.query.filter_by(type=attribute_type).first()

    @classmethod
    def find_by_id(cls, attribute_id):
        return cls.query.get(attribute_id)

    @classmethod
    def get(cls, search):
        query = cls.query

        if search:
            search_string = f"%{search}%"
            query = query.filter(
                or_(
                    Attribute.name.ilike(search_string),
                    Attribute.description.ilike(search_string),
                )
            )

        return query.order_by(db.asc(Attribute.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        attributes, total_count = cls.get(search)
        items = [attribute.to_dict() for attribute in attributes]
        return {"total_count": total_count, "items": items}

    @classmethod
    def create_attribute(cls, attribute):
        db.session.add(attribute)
        db.session.commit()

        for attribute_enum in attribute.attribute_enums:
            attribute_enum.attribute_id = attribute.id
            db.session.add(attribute_enum)

        attribute.attribute_enums = []

        db.session.commit()

    @classmethod
    def add_attribute(cls, data) -> tuple[str, int]:
        attribute = cls.from_dict(data)
        db.session.add(attribute)
        db.session.commit()
        return f"Added {attribute.name}", 201

    @classmethod
    def update(cls, attribute_id, data) -> tuple[str, int]:
        attribute = cls.query.get(attribute_id)
        if not attribute:
            return "Attribute not found", 404
        for key, value in data.items():
            if hasattr(attribute, key) and key != "id":
                setattr(attribute, key, value)
        db.session.commit()
        return f"Attribute {attribute.name} updated", 200

    @classmethod
    def delete(cls, id) -> tuple[str, int]:
        if cls.query.filter_by(id=id).delete():
            db.session.commit()
            return f"Attribute {id} deleted", 200

        return f"Attribute {id} not found", 404

    @classmethod
    def load_cve_from_file(cls, file_path):
        attribute = cls.query.filter_by(type=AttributeType.CVE).first()
        AttributeEnum.delete_imported_for_attribute(attribute.id)

        item_count = 0
        block_item_count = 0
        desc = ""
        for event, element in iterparse(file_path, events=("start", "end")):
            if event == "end":
                if element.tag == "{http://cve.mitre.org/cve/downloads/1.0}desc":
                    desc = element.text
                elif element.tag == "{http://cve.mitre.org/cve/downloads/1.0}item":
                    attribute_enum = AttributeEnum(None, item_count, element.attrib["name"], desc)
                    attribute_enum.attribute_id = attribute.id
                    attribute_enum.imported = True
                    db.session.add(attribute_enum)
                    item_count += 1
                    block_item_count += 1
                    element.clear()
                    desc = ""
                    if block_item_count == 1000:
                        logger.log_debug(f"Processed CVE items: {item_count}")
                        block_item_count = 0
                        db.session.commit()

        logger.log_debug(f"Processed CVE items: {str(item_count)}")
        db.session.commit()

    @classmethod
    def load_cpe_from_file(cls, file_path):
        attribute = cls.query.filter_by(type=AttributeType.CPE).first()
        AttributeEnum.delete_imported_for_attribute(attribute.id)

        item_count = 0
        block_item_count = 0
        desc = ""
        for event, element in iterparse(file_path, events=("start", "end")):
            if event == "end":
                logger.log_debug(f"Element: {element}")
                if element.tag == "{http://cpe.mitre.org/dictionary/2.0}title":
                    desc = element.text
                elif element.tag == "{http://cpe.mitre.org/dictionary/2.0}cpe-item":
                    attribute_enum = AttributeEnum(None, item_count, element.attrib["name"], desc)
                    attribute_enum.attribute_id = attribute.id
                    attribute_enum.imported = True
                    db.session.add(attribute_enum)
                    item_count += 1
                    block_item_count += 1
                    element.clear()
                    desc = ""
                    if block_item_count == 1000:
                        logger.log_debug(f"Processed CPE items: {item_count}")
                        block_item_count = 0
                        db.session.commit()

        logger.log_debug(f"Processed CPE items: {str(item_count)}")
        db.session.commit()

    @classmethod
    def load_dictionaries(cls, dict_type):
        if dict_type == "cve":
            cve_update_file = os.getenv("CVE_UPDATE_FILE")
            if cve_update_file is not None and os.path.exists(cve_update_file):
                Attribute.load_cve_from_file(cve_update_file)

        if dict_type == "cpe":
            cpe_update_file = os.getenv("CPE_UPDATE_FILE")
            if cpe_update_file is not None and os.path.exists(cpe_update_file):
                Attribute.load_cpe_from_file(cpe_update_file)

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["Attribute"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Attribute":
        return cls(**data)

    def get_tag(self):
        switcher = {
            AttributeType.STRING: "mdi-form-textbox",
            AttributeType.NUMBER: "mdi-numeric",
            AttributeType.BOOLEAN: "mdi-checkbox-marked-outline",
            AttributeType.RADIO: "mdi-radiobox-marked",
            AttributeType.ENUM: "mdi-format-list-bulleted-type",
            AttributeType.TEXT: "mdi-form-textarea",
            AttributeType.RICH_TEXT: "mdi-format-font",
            AttributeType.DATE: "mdi-calendar-blank-outline",
            AttributeType.TIME: "clock-outline",
            AttributeType.DATE_TIME: "calendar-clock",
            AttributeType.LINK: "mdi-link",
            AttributeType.ATTACHMENT: "mdi-paperclip",
            AttributeType.TLP: "mdi-traffic-light",
            AttributeType.CPE: "mdi-laptop",
            AttributeType.CVE: "mdi-hazard-lights",
            AttributeType.CVSS: "mdi-counter",
        }
        return switcher.get(self.type, "mdi-textbox")

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["attribute_enums"] = [attribute_enum.to_dict() for attribute_enum in self.attribute_enums]
        data["tag"] = self.get_tag()
        return data
