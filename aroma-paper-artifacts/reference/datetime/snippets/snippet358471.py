import arrow
import inspect
import functools
import asyncio
import uuid
from dateutil import tz
import datetime
from .units import SECOND, MINUTE, HOUR, DAY, MONTH, WEEK
import logging


def __init__(self, name: str=None, interval: int=1, scheduler=None, loop=None, tz: str=None, run_total: int=None, tolerance: int=10):
    '\n        :param name: crontab name\n        :param interval: crontab apply interval\n        :param scheduler: crontab scheduler instance for now ,it is useless\n        :param loop: asyncio running loop\n        :param tz: timezone info. support string tz format\n        :param run_total: crontab task total running times,\n        :       with this parameter,you can limit its cron task count\n        :param tolerance: crontab tolerance. time tolerance, within is range,\n        :       task will still be applied\n        '
    self.name = (name or str(uuid.uuid1()))
    self.interval = interval
    self.job_func = None
    self.unit = None
    self.at_time = (None, None)
    self.at_exact_time = None
    self.last_run = None
    self.next_run = None
    self.run_count = 0
    self.run_total = run_total
    self.start_hour = None
    self.end_hour = None
    self.period = None
    self.week_day = None
    self.month_day = None
    self.scheduler = scheduler
    self.loop = (loop or asyncio.get_event_loop())
    self.gte_day = False
    self.tz = tz
    self.tolerance = datetime.timedelta(seconds=tolerance)
