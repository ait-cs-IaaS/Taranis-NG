from flask import request
from flask_restx import Resource, Namespace

from core.managers.auth_manager import api_key_required
from core.managers.log_manager import logger
from core.model.osint_source import OSINTSource
from core.model.queue import ScheduleEntry, Schedule


class QueueSchedule(Resource):
    @api_key_required
    def get(self):
        try:
            if schedules := Schedule.get_all():
                return [sched.to_dict() for sched in schedules], 200
            return {"message": "No schedules found"}, 404
        except Exception:
            logger.log_debug_trace()

    @api_key_required
    def put(self):
        try:
            data = request.json
            if not data:
                return {"message": "No data provided"}, 400
            entries = [ScheduleEntry.from_dict(entry) for entry in data]
            if not entries:
                return {"message": "No entries provided"}, 400
            return Schedule.sync(entries), 200
        except Exception:
            logger.log_debug_trace()


class Sources(Resource):
    @api_key_required
    def get(self, source_id: str):
        try:
            if source := OSINTSource.get(source_id):
                return source.to_collector_dict(), 200
            return {"message": f"Source with id {source_id} not found"}, 404
        except Exception:
            logger.log_debug_trace()


def initialize(api):
    worker_namespace = Namespace("Worker", description="Publish Subscribe Worker Endpoints", path="/api/v1/worker")
    beat_namespace = Namespace("Beat", description="Publish Subscribe Beat Endpoints", path="/api/v1/beat")
    beat_namespace.add_resource(
        QueueSchedule,
        "/schedule",
    )
    worker_namespace.add_resource(
        Sources,
        "/osint-sources/<string:source_id>",
    )
    api.add_namespace(beat_namespace)
    api.add_namespace(worker_namespace)
