import mongoengine
import traceback
import datetime
from celery import schedules
from celerybeatmongo.models import PeriodicTask
from celery.beat import Scheduler, ScheduleEntry
from celery.utils.log import get_logger
from celery import current_app


def requires_update(self):
    'check whether we should pull an updated schedule\n        from the backend database'
    if (not self._last_updated):
        return True
    return ((self._last_updated + self.UPDATE_INTERVAL) < datetime.datetime.now())
