from celery import Celery
from flask import Flask

from core.managers.log_manager import logger

celery: Celery = Celery()


class QueueManager:
    def __init__(self, app: Flask):
        self.celery = self.init_app(app)

    def init_app(self, app: Flask):
        celery_app = Celery(app.name)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app


def initialize(app: Flask):
    global celery
    celery = QueueManager(app).celery


periodic_tasks = [
    {"task": "cleanup_token_blacklist", "schedule": "daily"},
]


def periodic_collection_tasks():
    from core.model.osint_source import OSINTSource

    return OSINTSource.get_schedule_by_type()


def collect_osint_source(source_id: str):
    celery.send_task("worker.tasks.collect", args=[source_id])
    logger.info(f"Collect for source {source_id} scheduled")
    return {"message": f"Refresh for source {source_id} scheduled"}, 200
