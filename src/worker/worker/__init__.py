import sys
from celery import Celery
from celery.schedules import crontab

from worker.config import Config
from worker.log import logger
from worker.core_api import CoreApi
from worker.tasks import collect


class CeleryWorker:
    def __init__(self):
        celery_config = Config.CELERY

        self.app = Celery(__name__)
        self.app.config_from_object(celery_config)
        self.app.set_default()
        self.core_api = CoreApi()


    def setup_periodic_tasks(self):
        jobs = self.core_api.get_periodic_tasks()

        if jobs is None:
            logger.log_info("No periodic tasks to schedule")
            return

        for job in jobs:
            if "schedule" not in job:
                job["schedule"] = "hourly"
            self.schedule_collector(job["id"], job["schedule"])
        logger.log_info("Periodic tasks scheduled")

    def schedule_job_every_day(self, job):
        self.app.add_periodic_task(
            schedule=crontab(hour="0", minute="0"),
            sig=job,
        )

    def schedule_job_every_hour(self, job):
        self.app.add_periodic_task(
            schedule=crontab(minute="0"),
            sig=job,
        )

    def schedule_collector(self, id, schedule):
        self.app.add_periodic_task(
            schedule=schedule,
            sig=collect.s(id),
        )


if __name__ == "worker":
    cw = CeleryWorker()
    if "beat" in sys.argv:
        logger.log_info("Starting celery beat")
        cw.setup_periodic_tasks()
    celery = cw.app
