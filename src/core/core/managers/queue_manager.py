from celery import Celery
from flask import Flask

from core.managers.log_manager import logger
from core.model.queue import Schedule
from core.model.osint_source import OSINTSource

queue_manager: "QueueManager"
periodic_tasks = [
    {"id": "cleanup_token_blacklist", "name": "worker.tasks.cleanup_token_blacklist", "schedule": "daily", "args": []},
]


class QueueManager:
    def __init__(self, app: Flask):
        self.celery = self.init_app(app)
        Schedule.ensure_single_instance()
        self.queue = Schedule.get_instance()
        self.add_periodic_tasks()
        self.update_task_queue_from_osint_sources()

    def init_app(self, app: Flask):
        celery_app = Celery(app.name)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app

    def add_periodic_tasks(self):
        for task in periodic_tasks:
            self.queue.add_or_update(task)

    def update_task_queue_from_osint_sources(self):
        from core.model.osint_source import OSINTSource

        sources = OSINTSource.get_all()
        for source in sources:
            self.queue.add_or_update(source.to_task_dict())

    def ping_workers(self):
        result = self.celery.control.ping()
        workers = [{"name": list(worker.keys())[0], "status": list(list(worker.values())[0].keys())[0]} for worker in result]
        logger.info(f"Workers: {workers}")
        return workers


def initialize(app: Flask):
    global queue_manager
    queue_manager = QueueManager(app)


def schedule_osint_source(source: OSINTSource):
    entry = source.to_task_dict()
    queue_manager.queue.add_or_update(entry)
    logger.info(f"Schedule for source {source.id} updated")
    return {"message": f"Schedule for source {source.id} updated"}, 200


def unschedule_osint_source(source: OSINTSource):
    entry_id = source.to_task_dict()["id"]
    queue_manager.queue.delete_entry(entry_id)
    logger.info(f"Schedule for source {source.id} removed")
    return {"message": f"Schedule for source {source.id} removed"}, 200


def update_osint_source(source: OSINTSource):
    entry = source.to_task_dict()
    queue_manager.queue.update_entry(entry)
    logger.info(f"Schedule for source {source.id} updated")
    return {"message": f"Schedule for source {source.id} updated"}, 200


def collect_osint_source(source_id: str):
    queue_manager.celery.send_task("worker.tasks.collect", args=[source_id])
    logger.info(f"Collect for source {source_id} scheduled")
    return {"message": f"Refresh for source {source_id} scheduled"}, 200
