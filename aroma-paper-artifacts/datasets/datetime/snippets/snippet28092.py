import logging
from datetime import datetime, timedelta
import traceback
import time
import sys
from django.conf import settings
from django.utils.timezone import now as utc_now
from django.db.models import Q
from django_cron.helpers import get_class, get_current_time
from django_cron.models import CronJobLog
from django_cron.models import CronJobLog
from django_cron.models import CronJobLog
from django_cron.models import CronJobLog


def should_run_now(self, force=False):
    from django_cron.models import CronJobLog
    cron_job = self.cron_job
    '\n        Returns a boolean determining whether this cron should run now or not!\n        '
    self.user_time = None
    self.previously_ran_successful_cron = None
    if force:
        return True
    if (cron_job.schedule.run_monthly_on_days is not None):
        if (not (datetime.today().day in cron_job.schedule.run_monthly_on_days)):
            return False
    if (cron_job.schedule.run_weekly_on_days is not None):
        if (not (datetime.today().weekday() in cron_job.schedule.run_weekly_on_days)):
            return False
    if cron_job.schedule.retry_after_failure_mins:
        last_job = CronJobLog.objects.filter(code=cron_job.code).order_by('-start_time').exclude(start_time__gt=datetime.today()).first()
        if (last_job and (not last_job.is_success) and ((get_current_time() + timedelta(seconds=cron_job.schedule.run_tolerance_seconds)) <= (last_job.start_time + timedelta(minutes=cron_job.schedule.retry_after_failure_mins)))):
            return False
    if (cron_job.schedule.run_every_mins is not None):
        try:
            self.previously_ran_successful_cron = CronJobLog.objects.filter(code=cron_job.code, is_success=True).exclude(start_time__gt=datetime.today()).latest('start_time')
        except CronJobLog.DoesNotExist:
            pass
        if self.previously_ran_successful_cron:
            if ((get_current_time() + timedelta(seconds=cron_job.schedule.run_tolerance_seconds)) > (self.previously_ran_successful_cron.start_time + timedelta(minutes=cron_job.schedule.run_every_mins))):
                return True
        else:
            return True
    if cron_job.schedule.run_at_times:
        for time_data in cron_job.schedule.run_at_times:
            user_time = time.strptime(time_data, '%H:%M')
            now = get_current_time()
            actual_time = time.strptime(('%s:%s' % (now.hour, now.minute)), '%H:%M')
            if (actual_time >= user_time):
                qset = CronJobLog.objects.filter(code=cron_job.code, ran_at_time=time_data, is_success=True).filter((Q(start_time__gt=now) | Q(end_time__gte=now.replace(hour=0, minute=0, second=0, microsecond=0))))
                if (not qset):
                    self.user_time = time_data
                    return True
    return False
