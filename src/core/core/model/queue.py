from datetime import datetime
from typing import Any

from core.managers.db_manager import db
from core.managers.log_manager import logger
from core.model.base_model import BaseModel


class ScheduleEntry(BaseModel):
    id = db.Column(db.String, primary_key=True)
    task = db.Column(db.String)
    schedule = db.Column(db.String)
    args = db.Column(db.String)
    last_run_at = db.Column(db.DateTime)
    total_run_count = db.Column(db.Integer)

    def __init__(self, id, task, schedule, args):
        self.id = id
        self.task = task
        self.schedule = schedule
        self.args = args
        self.total_run_count = 0

    def update(self, data):
        update_data = self.from_dict(data)
        self.schedule = update_data.schedule
        self.args = update_data.args
        db.session.commit()

    @classmethod
    def add_or_update(cls, entry_data):
        if entry := cls.get(entry_data["id"]):
            entry.update(entry_data)
            db.session.commit()
            return entry, 200
        entry = cls.from_dict(entry_data)
        db.session.add(entry)
        db.session.commit()
        return entry, 200

    @classmethod
    def sync(cls, entries: list["ScheduleEntry"]):
        for entry in entries:
            if existing_entry := cls.get(entry.id):
                existing_entry.schedule = entry.schedule
                existing_entry.args = entry.args
                existing_entry.last_run_at = entry.last_run_at
                existing_entry.total_run_count = entry.total_run_count
            else:
                db.session.add(entry)
            db.session.commit()
        return "Schedule updated", 200

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["last_run_at"] = self.last_run_at.isoformat() if self.last_run_at else None
        return data

    def to_worker_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["name"] = data.pop("id")
        data["last_run_at"] = self.last_run_at.isoformat() if self.last_run_at else None
        return data
