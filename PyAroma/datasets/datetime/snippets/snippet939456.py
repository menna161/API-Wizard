import mongoengine
import traceback
import datetime
from celery import schedules
from celerybeatmongo.models import PeriodicTask
from celery.beat import Scheduler, ScheduleEntry
from celery.utils.log import get_logger
from celery import current_app


def is_due(self):
    if (not self._task.enabled):
        return schedules.schedstate(False, 5.0)
    if (hasattr(self._task, 'start_after') and self._task.start_after):
        if (datetime.datetime.now() < self._task.start_after):
            return schedules.schedstate(False, 5.0)
    if (hasattr(self._task, 'max_run_count') and self._task.max_run_count):
        if ((self._task.total_run_count or 0) >= self._task.max_run_count):
            self._task.enabled = False
            self._task.save()
            return schedules.schedstate(False, None)
    if self._task.run_immediately:
        (_, n) = self.schedule.is_due(self.last_run_at)
        return (True, n)
    return self.schedule.is_due(self.last_run_at)
