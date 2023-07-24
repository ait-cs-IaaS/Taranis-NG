import time
from celery.beat import Scheduler, ScheduleEntry
from datetime import datetime, timezone
from celery.schedules import crontab
from datetime import timedelta

from worker.core_api import CoreApi
from worker.log import logger

# class RESTScheduleEntry(ScheduleEntry):
#     def is_due(self):
#         return super(RESTScheduleEntry, self).is_due()

#     def next(self):
#         return super(RESTScheduleEntry, self).next()


class RESTScheduleEntry(ScheduleEntry):
    def is_due(self):
        return super(RESTScheduleEntry, self).is_due()
        # self.due_check_count += 1
        # if self.due_check_count >= 100:
        #     self.due_check_count = 0
        #     next_run_time = datetime.now(timezone.utc) + timedelta(seconds=int(next_time_to_run)) # type: ignore
        #     logger.debug(f'Task {self.name}: next_run_time={next_run_time}')
        #     self.core_api.update_next_run_time(next_run_time)
        # return is_due, next_time_to_run

    def next(self):
        return super(RESTScheduleEntry, self).next()


class RESTScheduler(Scheduler):
    Entry = RESTScheduleEntry

    def __init__(self, *args, **kwargs):
        super(RESTScheduler, self).__init__(*args, **kwargs)
        self.core_api = CoreApi()
        self.schedule = self.get_schedule_from_core()
        self.last_checked = datetime.now(timezone.utc)
        self.max_interval = 60


    def get_schedule_from_core(self):
        if schedule := self.core_api.get_schedule():
            logger.debug(f"Got schedule: {schedule}")
            schedule_dict = {}
            for entry in schedule:
                entry['app'] = self.app
                schedule_dict[entry['name']] = self.Entry(**entry)
                logger.debug(f'Added task {entry} to schedule')
                _, next_time_to_run = schedule_dict[entry["name"]].is_due()
                next_run_time = datetime.now(timezone.utc) + timedelta(seconds=int(next_time_to_run))
                logger.debug(f'Task {entry["name"]}: next_run_time={next_run_time}')
                self.core_api.update_next_run_time(entry["name"], next_run_time)
            return schedule_dict
        return {}

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

    def tick(self):
        now = datetime.now(timezone.utc)
        if (now - self.last_checked).total_seconds() >= self.max_interval:
            self.last_checked = now
            if self.schedule_changed():
                self.schedule = self.get_schedule()
        time.sleep(0.1)
        super(RESTScheduler, self).tick()
