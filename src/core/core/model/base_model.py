from typing import Any, TypeVar, Type

from core.managers.db_manager import db
import json

T = TypeVar("T", bound="BaseModel")


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.to_json()}"

    @classmethod
    def delete(cls: Type[T], id) -> tuple[str, int]:
        if cls.query.filter_by(id=id).delete():
            db.session.commit()
            return f"{cls.__name__} {id} deleted", 200

        return f"{cls.__name__} {id} not found", 404

    @classmethod
    def add(cls, data) -> tuple[str, int]:
        item = cls.from_dict(data)
        db.session.add(item)
        db.session.commit()
        return f"{cls.__name__} {item.id} created", 201

    @classmethod
    def add_multiple(cls, data) -> tuple[str, int]:
        items = cls.load_multiple(data)
        for item in items:
            db.session.add(item)
        db.session.commit()
        return f"{cls.__name__} {len(items)} items created", 201

    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        return cls(**data)

    @classmethod
    def load_multiple(cls: Type[T], json_data: list[dict[str, Any]]) -> list[T]:
        return [cls.from_dict(data) for data in json_data]

    def to_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def get(cls: Type[T], id) -> T | None:
        return cls.query.get(id)

    @classmethod
    def get_all(cls: Type[T]) -> list[T] | None:
        return cls.query.all()
