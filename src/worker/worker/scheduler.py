from celery.beat import Scheduler, ScheduleEntry
from datetime import datetime, timezone
from celery.schedules import crontab

from worker.core_api import CoreApi
from worker.log import logger

class RESTScheduleEntry(ScheduleEntry):
    def is_due(self):
        return super(RESTScheduleEntry, self).is_due()

    def next(self):
        return super(RESTScheduleEntry, self).next()

class RESTScheduler(Scheduler):
    Entry = RESTScheduleEntry

    def __init__(self, *args, **kwargs):
        super(RESTScheduler, self).__init__(*args, **kwargs)
        self.core_api = CoreApi()
        self.schedule = self.get_schedule_from_core()
        self.max_interval = 60


    def get_schedule_from_core(self):
        if schedule := self.core_api.get_schedule():
            logger.info(f"Got schedule: {schedule}")
            schedule_dict = {}
            for entry in schedule:
                entry['schedule'] = self.parse_schedule(entry)
                entry['app'] = self.app
                schedule_dict[entry['name']] = self.Entry(**entry)
            return schedule_dict
        return {}

    def parse_schedule(self, entry):
        if schedule_content := entry.get("schedule"):
            if schedule_content == 'hourly':
                return crontab(minute="0")
            if schedule_content == 'daily':
                return crontab(minute="0", hour="0")
            if schedule_content == 'weekly':
                return crontab(minute="0", hour="0", day_of_week="0")
        return crontab(minute="0")

    def set_to_backend(self):
        self.core_api.update_schedule(self.schedule)

    def sync(self):
        self.set_to_backend()

    def schedule_changed(self):
        return self.schedule != self.get_schedule_from_core()

    def reserve(self, entry):
        new_entry = super(RESTScheduler, self).reserve(entry)
        new_entry.last_run_at = datetime.now(timezone.utc)
        new_entry.total_run_count += 1
        return new_entry

    def get_schedule(self):
        self.schedule = self.get_schedule_from_core()
        return self.schedule
