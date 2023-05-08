import arrow
import inspect
import functools
import asyncio
import uuid
from dateutil import tz
import datetime
from .units import SECOND, MINUTE, HOUR, DAY, MONTH, WEEK
import logging


def at(self, time_string: str=None, time_shift=8):
    if (time_string is None):
        pass
    else:
        time_string = time_string.replace('：', ':')
        (first, *_) = time_string.split(':')
        if (len(first) > 2):
            try:
                arrow_time = arrow.get(time_string)
                arrow_time = self.get_tz_time(arrow_time).shift(hours=(- time_shift))
                self.at_exact_time = arrow_time
                self.run_total = 1
            except Exception as tmp:
                logger.exception(tmp)
                logger.info(f'{self.name} parse datetime error')
        else:
            try:
                self.at_time = self.split_time(time_string)
            except Exception as tmp:
                logger.exception(tmp)
                logger.info(f'{self.name} parse hour and minute error')
    return self
