from worker.config import Config
from celery import Celery
from celery.schedules import crontab
import sys

from worker.log import logger


class CeleryWorker:
    def __init__(self):
        celery_config = Config.CELERY

        self.app = Celery(__name__)
        self.app.config_from_object(celery_config)
        self.app.set_default()

    def setup_periodic_tasks(self):
        jobs = [
            # run task 1 every minute and task 2 every 2 minutes
            # {"task": task1.s("testX"), "schedule": 10.0},
            # {"task": task2.s(), "schedule": crontab(minute="*/2")},
        ]

        for job in jobs:
            self.app.add_periodic_task(schedule=job["schedule"], sig=job["task"])

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


if __name__ == "worker":
    cw = CeleryWorker()
    if "beat" in sys.argv:
        logger.log_info("Starting celery beat")
        cw.setup_periodic_tasks()
    celery = cw.app
