import arrow
import inspect
import functools
import asyncio
import uuid
from dateutil import tz
import datetime
from .units import SECOND, MINUTE, HOUR, DAY, MONTH, WEEK
import logging


def decide_run(self):
    now = self.get_now()
    if self.at_exact_time:
        if ((now >= self.at_exact_time) and ((now - self.at_exact_time) <= self.tolerance)):
            return True
        else:
            return False
    if self.next_run:
        if (now >= self.next_run):
            return True
    else:
        if (self.month_day and (self.month_day != now.day)):
            return False
        if (self.week_day and (self.week_day != now.weekday())):
            return False
        now_datetime = now.datetime
        (hour, minute) = self.at_time
        if ((hour is not None) and (minute is not None)):
            if ((now_datetime.hour == hour) and (now_datetime.minute == minute)):
                return True
        elif (hour is not None):
            if (now_datetime.hour == hour):
                if ((self.start_hour is not None) and (self.end_hour is not None)):
                    if (int(self.start_hour) <= hour <= int(self.end_hour)):
                        return True
                elif (self.start_hour is not None):
                    if (int(self.start_hour) <= hour):
                        return True
                elif (self.end_hour is not None):
                    if (hour <= int(self.end_hour)):
                        return True
                else:
                    return True
        elif (minute is not None):
            if (now_datetime.minute == minute):
                hour = now_datetime.hour
                if ((self.start_hour is not None) and (self.end_hour is not None)):
                    if (int(self.start_hour) <= hour <= int(self.end_hour)):
                        return True
                elif (self.start_hour is not None):
                    if (int(self.start_hour) <= hour):
                        return True
                elif (self.end_hour is not None):
                    if (hour <= int(self.end_hour)):
                        return True
                else:
                    return True
        else:
            return True
    return False
