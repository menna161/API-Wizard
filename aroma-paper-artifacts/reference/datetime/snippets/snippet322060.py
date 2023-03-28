import os, sys, re, time, threading, _thread
import warnings, tempfile
import configparser, inspect, getpass, traceback
from datetime import datetime, timedelta, timezone
from collections.abc import Iterable
from html.parser import HTMLParser
import mastodon
from mastodon import Mastodon, StreamListener
from configobj import ConfigObj


def interval_next(f, t=datetime.now(), tLast=datetime.now()):
    "\n    Calculate the number of seconds from now until the function should next run.\n    This function handles both cron-like and interval-like scheduling via the\n    following:\n     ∗ If no interval and no schedule are specified, return 0\n     ∗ If an interval is specified but no schedule, return the number of seconds\n       from <t> until <interval> has passed since <tLast> or 0 if it's overdue.\n     ∗ If a schedule is passed but no interval, figure out when next to run by\n       parsing the schedule according to the following rules:\n         ∗ If all of second, minute, hour, day_of_week/day_of_month, month, year\n           are specified, then the time to run is singular and the function will\n           run only once at that time. If it has not happened yet, return the\n           number of seconds from <t> until that time, otherwise return -1.\n         ∗ If one or more are unspecified, then they are treated as open slots.\n           return the number of seconds from <t> until the time next fits within\n           the specified constraints, or if it never will again return -1.\n             ∗ Only one of day_of_week and day_of_month may be specified. if both\n               are specified, then day_of_month is used and day_of_week is ignored.\n         ∗ If all are unspecified treat it as having no schedule specified\n     ∗ If both a schedule and an interval are specified, TODO but it should do\n       something along the lines of finding the next multiple of interval from tLast\n       that fits the schedule spec and returning the number of seconds until then.\n\n    NOTE: If the time until the next event is greater than an hour in the\n    future, this function will return the number of seconds until the top of the\n    next hour (1-3600). Be sure to continue checking until this function\n    returns 0.\n    "
    has_interval = hasattr(f, 'interval')
    has_schedule = hasattr(f, 'schedule')
    if ((not has_interval) and (not has_schedule)):
        return 0
    if (has_interval and (not has_schedule)):
        tNext = (tLast + timedelta(seconds=f.interval))
        return max(total_seconds((tNext - t)), 0)
    if has_schedule:
        interval_min = 3600
        for s in f.schedule:
            interval = schedule_next(s, t)
            if (interval < interval_min):
                interval_min = interval
        return interval_min
