import mongoengine
import traceback
import datetime
from celery import schedules
from celerybeatmongo.models import PeriodicTask
from celery.beat import Scheduler, ScheduleEntry
from celery.utils.log import get_logger
from celery import current_app


@property
def schedule(self):
    if self.requires_update():
        self._schedule = self.get_from_database()
        self._last_updated = datetime.datetime.now()
    return self._schedule
