import sqlalchemy
from typing import Any
from sqlalchemy import func, or_, and_
from sqlalchemy.sql.expression import cast

from core.managers.db_manager import db
from core.model.acl_entry import ACLEntry
from core.model.acl_entry import ItemType


class WordList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    use_for_stop_words = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(), nullable=True, default=None)
    entries = db.relationship("WordListEntry", cascade="all, delete-orphan")

    def __init__(self, name, description="", use_for_stop_words=False, link=None, entries=None, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.use_for_stop_words = use_for_stop_words
        self.link = link
        self.entries = entries

    @classmethod
    def find(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def allowed_with_acl(cls, word_list_id, user, see, access, modify):
        query = db.session.query(WordList.id).distinct().group_by(WordList.id).filter(WordList.id == word_list_id)

        query = query.outerjoin(
            ACLEntry,
            and_(
                cast(WordList.id, sqlalchemy.String) == ACLEntry.item_id,
                ACLEntry.item_type == ItemType.WORD_LIST,
            ),
        )

        query = ACLEntry.apply_query(query, user, see, access, modify)

        return query.scalar() is not None

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(WordList.name)).all()

    @classmethod
    def get(cls, search, user, acl_check):
        query = cls.query.distinct().group_by(WordList.id)

        if acl_check is True:
            query = query.outerjoin(
                ACLEntry,
                and_(
                    cast(WordList.id, sqlalchemy.String) == ACLEntry.item_id,
                    ACLEntry.item_type == ItemType.WORD_LIST,
                ),
            )
            query = ACLEntry.apply_query(query, user, True, False, False)

        if search is not None:
            search_string = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(WordList.name).like(search_string),
                    func.lower(WordList.description).like(search_string),
                )
            )

        return query.order_by(db.asc(WordList.name)).all(), query.count()

    @classmethod
    def get_all_json(cls, search, user, acl_check):
        word_lists, count = cls.get(search, user, acl_check)
        items = [word_list.to_dict() for word_list in word_lists]
        return {"total_count": count, "items": items}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["WordList"]:
        return [cls.from_dict(data) for data in json_data]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WordList":
        return cls(**data)

    def to_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["entries"] = [entry.to_dict() for entry in self.entries]
        data["tag"] = "mdi-format-list-bulleted-square"
        return data

    @classmethod
    def add_new(cls, data) -> tuple[str, int]:
        word_list = cls.from_dict(data)
        db.session.add(word_list)
        db.session.commit()
        return f"Successfully Added {word_list.id}", 201

    @classmethod
    def update(cls, word_list_id, data) -> tuple[str, int]:
        word_list = cls.query.get(word_list_id)
        if word_list is None:
            return "WordList not found", 404
        word_list.entries = [WordListEntry.from_dict(entry) for entry in data.pop("entries")]
        for key, value in data.items():
            if hasattr(word_list, key) and key != "id" and key != "entries":
                setattr(word_list, key, value)
        db.session.commit()
        return "Word list updated", 200

    @classmethod
    def delete(cls, id) -> tuple[str, int]:
        word_list = cls.query.get(id)
        if not word_list:
            return "Word list not found", 404
        db.session.delete(word_list)
        db.session.commit()
        return "Word list deleted", 200


class WordListEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    word_list_id = db.Column(db.Integer, db.ForeignKey("word_list.id"))

    def __init__(self, value, description=""):
        self.id = None
        self.value = value
        self.description = description

    @classmethod
    def identical(cls, value, word_list_id):
        return db.session.query(db.exists().where(WordListEntry.value == value).where(WordListEntry.word_list_id == word_list_id)).scalar()

    @classmethod
    def delete_entries(cls, id, value):
        word_list = WordList.find(id)
        cls.query.filter_by(word_list_id=word_list.id).filter_by(value=value).delete()
        db.session.commit()

    @classmethod
    def update_word_list_entries(cls, id, entries_data):
        word_list = WordList.find(id)

        entries = cls.load_multiple(entries_data)
        for entry in entries:
            if not cls.identical(entry.value, word_list.id):
                word_list.entries.append(entry)
                db.session.commit()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WordListEntry":
        return cls(**data)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def load_multiple(cls, json_data: list[dict[str, Any]]) -> list["WordListEntry"]:
        return [cls.from_dict(data) for data in json_data]
