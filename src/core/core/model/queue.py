from datetime import datetime

from core.managers.db_manager import db
from core.managers.log_manager import logger
from core.model.base_model import BaseModel


class Schedule(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    entries = db.relationship("ScheduleEntry", cascade="all, delete")

    @classmethod
    def sync(cls, entries: list["ScheduleEntry"]):
        for entry in entries:
            if existing_entry := ScheduleEntry.find_by_name(entry.name):
                existing_entry.schedule = entry.schedule
                existing_entry.args = entry.args
                existing_entry.last_run_at = entry.last_run_at
                existing_entry.total_run_count = entry.total_run_count
            else:
                db.session.add(entry)
            db.session.commit()
        return "Schedule updated", 200

    @classmethod
    def get_instance(cls):
        instance = cls.query.first()
        if not instance:
            instance = cls()
            db.session.add(instance)
            db.session.commit()
        return instance

    @classmethod
    def ensure_single_instance(cls):
        instances = cls.query.all()
        if len(instances) > 1:
            for instance in instances[1:]:
                db.session.delete(instance)
            db.session.commit()
        return len(instances)

    def delete_entry(self, entry_id):
        entry = ScheduleEntry.get(entry_id)
        if not entry:
            return f"Schedule Entry {entry_id} not found", 404
        db.session.delete(entry)
        db.session.commit()
        return "Schedule Entry deleted", 200

    def update_entry(self, entry_data):
        if entry := ScheduleEntry.get(entry_data["id"]):
            entry.update(entry_data)
            db.session.commit()
            return entry, 200
        return f"Schedule Entry {entry_data['id']} not found", 404

    def add_or_update(self, entry_data):
        if entry := ScheduleEntry.get(entry_data["id"]):
            entry.update(entry_data)
            db.session.commit()
            return entry, 200
        entry = ScheduleEntry.from_dict(entry_data)
        self.entries.append(entry)
        db.session.commit()
        return entry, 200


class ScheduleEntry(BaseModel):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedule.id"))

    schedule = db.Column(db.String)
    args = db.Column(db.String)
    last_run_at = db.Column(db.DateTime)
    total_run_count = db.Column(db.Integer)

    def __init__(self, id, name, schedule, args):
        self.id = id
        self.name = name
        self.schedule = schedule
        self.args = args
        self.total_run_count = 0

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def update(self, data):
        update_data = self.from_dict(data)
        self.schedule = update_data.schedule
        self.args = update_data.args
        db.session.commit()
