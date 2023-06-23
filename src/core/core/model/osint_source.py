import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import or_, and_

from core.managers.db_manager import db
from core.managers.log_manager import logger
from core.model.acl_entry import ACLEntry, ItemType
from core.model.collector import Collector
from core.model.parameter_value import ParameterValue
from core.model.word_list import WordList
from core.model.base_model import BaseModel


class OSINTSource(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())

    collector_id = db.Column(db.String, db.ForeignKey("collector.id"))
    parameter_values = db.relationship("ParameterValue", secondary="osint_source_parameter_value", cascade="all")

    word_lists = db.relationship("WordList", secondary="osint_source_word_list")

    modified = db.Column(db.DateTime, default=datetime.now)
    last_collected = db.Column(db.DateTime, default=None)
    last_attempted = db.Column(db.DateTime, default=None)
    state = db.Column(db.SmallInteger, default=0)
    last_error_message = db.Column(db.String, default=None)

    def __init__(self, name, description, collector_id, parameter_values, word_lists, osint_source_groups, id=None):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.collector_id = collector_id
        self.parameter_values = parameter_values

        self.word_lists = []
        self.word_lists.extend(WordList.get(word_list.id) for word_list in word_lists)
        self.osint_source_groups = (
            [OSINTSourceGroup.get_default()]
            if osint_source_groups is None
            else [OSINTSourceGroup.get(osint_source_group.id) for osint_source_group in osint_source_groups]
        )

    @classmethod
    def get_all(cls):
        return cls.query.order_by(OSINTSource.name).all()

    @classmethod
    def get_by_filter(cls, search=None):
        query = cls.query

        if search:
            search_string = f"%{search}%"
            query = query.join(Collector, OSINTSource.collector_id == Collector.id).filter(
                or_(
                    OSINTSource.name.ilike(search_string),
                    OSINTSource.description.ilike(search_string),
                    Collector.type.ilike(search_string),
                )
            )

        return query.order_by(db.asc(OSINTSource.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search):
        sources, count = cls.get_by_filter(search)
        items = [source.to_dict() for source in sources]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["OSINTSource"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OSINTSource":
        parameter_values = [parameter_value.to_dict() for parameter_value in data.pop("parameter_values", [])]
        word_lists = [WordList.get(word_list_id) for word_list_id in data.pop("word_lists", [])]
        return cls(parameter_values=parameter_values, word_lists=word_lists, **data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        data["word_lists"] = [word_list.id for word_list in self.word_lists]
        data["parameter_values"] = [parameter_value.to_dict() for parameter_value in self.parameter_values]
        data["tag"] = "mdi-animation-outline"
        return data

    @classmethod
    def get_all_with_type(cls):
        sources, count = cls.get_by_filter(None)
        items = [source.to_list() for source in sources]
        return {"total_count": count, "items": items}

    def to_list(self):
        return {"id": self.id, "name": self.name, "description": self.description, "collector_type": self.collector.type}

    @classmethod
    def get_all_by_type(cls, collector_type: str):
        query = cls.query.join(Collector, OSINTSource.collector_id == Collector.id).filter(Collector.type == collector_type)
        sources = query.order_by(db.asc(OSINTSource.name)).all()
        return [source.to_dict() for source in sources]

    @classmethod
    def get_all_for_collector(cls, collector):
        sources = cls.query.filter_by(collector_type=collector).all()
        return [source.to_dict() for source in sources]

    @classmethod
    def add_new(cls, data):
        osint_source = cls.from_dict(data)
        db.session.add(osint_source)
        db.session.commit()
        return f"Successfully Added {osint_source.id}", 201

    @classmethod
    def import_new(cls, osint_source) -> str:
        collector = Collector.find_by_type(osint_source.collector.type)
        parameter_values = []
        for parameter_value in osint_source.parameter_values:
            for parameter in collector.parameters:
                pv_key = parameter_value["parameter"] if type(parameter_value["parameter"]) == str else parameter_value["parameter"].key
                if parameter.key == pv_key:
                    new_parameter_value = ParameterValue(parameter_value["value"], parameter.key)
                    parameter_values.append(new_parameter_value)
                    break
        source_id = str(uuid.uuid4())
        news_osint_source = OSINTSource(
            source_id,
            osint_source.name,
            osint_source.description,
            collector.id,
            parameter_values,
            [],
            [],
        )

        db.session.add(news_osint_source)
        db.session.commit()
        return source_id

    @classmethod
    def update(cls, osint_source_id, data):
        osint_source = cls.query.get(osint_source_id)
        updated_osint_source = cls.from_dict(data)
        osint_source.name = updated_osint_source.name
        osint_source.description = updated_osint_source.description

        for value in osint_source.parameter_values:
            for updated_value in updated_osint_source.parameter_values:
                if value.parameter_key == updated_value.parameter_key:
                    value.value = updated_value.value

        osint_source.word_lists = updated_osint_source.word_lists

        current_groups = OSINTSourceGroup.get_for_osint_source(osint_source_id)
        default_group = None
        for group in current_groups:
            if group.default:
                default_group = group

            for source in group.osint_sources:
                if source.id == osint_source_id:
                    group.osint_sources.remove(source)
                    break

        if len(updated_osint_source.osint_source_groups) > 0:
            for osint_source_group in updated_osint_source.osint_source_groups:
                osint_source_group.osint_sources.append(osint_source)
        else:
            default_group = OSINTSourceGroup.get_default()
            default_group.osint_sources.append(osint_source)

        db.session.commit()

        return osint_source, default_group

    def update_status(self, status_schema):
        # if not collected, do not change last collected timestamp
        if status_schema.last_collected:
            self.last_collected = status_schema.last_collected

        # if not attempted, do not change last collected timestamp
        if status_schema.last_attempted:
            self.last_attempted = status_schema.last_attempted

        self.last_error_message = status_schema.last_error_message


class OSINTSourceParameterValue(BaseModel):
    osint_source_id = db.Column(db.String, db.ForeignKey("osint_source.id"), primary_key=True)
    parameter_value_id = db.Column(db.Integer, db.ForeignKey("parameter_value.id"), primary_key=True)


class OSINTSourceWordList(BaseModel):
    osint_source_id = db.Column(db.String, db.ForeignKey("osint_source.id"), primary_key=True)
    word_list_id = db.Column(db.Integer, db.ForeignKey("word_list.id"), primary_key=True)


class OSINTSourceGroup(BaseModel):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    default = db.Column(db.Boolean(), default=False)

    osint_sources = db.relationship("OSINTSource", secondary="osint_source_group_osint_source")

    def __init__(self, id, name, description, default, osint_sources):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.default = default
        self.osint_sources = [OSINTSource.get(osint_source.id) for osint_source in osint_sources]

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(OSINTSourceGroup.name)).all()

    @classmethod
    def get_for_osint_source(cls, osint_source_id):
        return cls.query.join(
            OSINTSourceGroupOSINTSource,
            and_(
                OSINTSourceGroupOSINTSource.osint_source_id == osint_source_id,
                OSINTSourceGroup.id == OSINTSourceGroupOSINTSource.osint_source_group_id,
            ),
        ).all()

    @classmethod
    def get_default(cls):
        return cls.query.filter(OSINTSourceGroup.default).first()

    @classmethod
    def allowed_with_acl(cls, group_id, user, see: bool, access: bool, modify: bool) -> bool:
        query = db.session.query(OSINTSourceGroup.id).distinct().group_by(OSINTSourceGroup.id).filter(OSINTSourceGroup.id == group_id)

        query = query.outerjoin(
            ACLEntry,
            and_(
                OSINTSourceGroup.id == ACLEntry.item_id,
                ACLEntry.item_type == ItemType.OSINT_SOURCE_GROUP,
            ),
        )
        query = ACLEntry.apply_query(query, user, see, access, modify)
        acl_check_result = query.scalar() is not None
        logger.log_debug(f"ACL Check for {group_id} results: {acl_check_result}")

        return acl_check_result

    @classmethod
    def get_by_filter(cls, search, user, acl_check):
        query = cls.query.distinct().group_by(OSINTSourceGroup.id)

        if acl_check:
            query = query.outerjoin(
                ACLEntry, and_(OSINTSourceGroup.id == ACLEntry.item_id, ACLEntry.item_type == ItemType.OSINT_SOURCE_GROUP)
            )
            query = ACLEntry.apply_query(query, user, True, False, False)

        if search:
            search_string = f"%{search}%"
            query = query.filter(
                or_(
                    OSINTSourceGroup.name.ilike(f"%{search}%"),
                    OSINTSourceGroup.description.ilike(f"%{search}%"),
                )
            )

        return (
            query.all(),
            query.count(),
        )

    @classmethod
    def get_all_json(cls, search, user, acl_check):
        groups, count = cls.get_by_filter(search, user, acl_check)
        items = [group.to_dict() for group in groups]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["OSINTSourceGroup"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OSINTSourceGroup":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["osint_sources"] = [osint_source.id for osint_source in self.osint_sources]
        return data

    @classmethod
    def add(cls, data):
        osint_source_group = cls.from_dict(data)
        db.session.add(osint_source_group)
        db.session.commit()
        return f"Successfully Added {osint_source_group.id}", 201

    @classmethod
    def create(cls, group_id, name, description, default=False):
        if osint_source_group := cls.get(group_id):
            return {"message": f"OSINT Source Group {osint_source_group.id} already exists"}, 400
        osint_source_group = OSINTSourceGroup(group_id, name, description, default, [])
        db.session.add(osint_source_group)
        db.session.commit()
        return {"message": f"Successfully created {osint_source_group.id}"}, 201

    @classmethod
    def delete(cls, osint_source_group_id):
        osint_source_group = cls.query.get(osint_source_group_id)
        if osint_source_group.default is not False:
            return {"message": "could_not_delete_default_group"}, 400
        db.session.delete(osint_source_group)
        db.session.commit()
        return {"message": f"Successfully deleted {osint_source_group.id}"}, 200

    @classmethod
    def update(cls, osint_source_group_id, data):
        osint_source_group = cls.query.get(osint_source_group_id)
        if osint_source_group is None:
            return "OSINT Source Group not found", 404
        osint_source_group.name = data["name"]
        osint_source_group.description = data["description"]
        osint_source_group.osint_sources = [OSINTSource.get(osint_source) for osint_source in data.pop("osint_sources", [])]
        db.session.commit()
        return f"Succussfully updated {osint_source_group.id}", 201

        # TODO: Reassign news items to default group
        # if sources_in_default_group is not None:
        #     default_group = osint_source.OSINTSourceGroup.get_default()
        #     for source in sources_in_default_group:
        #         NewsItemAggregate.reassign_to_new_groups(source.id, default_group.id)


class OSINTSourceGroupOSINTSource(BaseModel):
    osint_source_group_id = db.Column(db.String, db.ForeignKey("osint_source_group.id", ondelete="CASCADE"), primary_key=True)
    osint_source_id = db.Column(db.String, db.ForeignKey("osint_source.id", ondelete="CASCADE"), primary_key=True)
