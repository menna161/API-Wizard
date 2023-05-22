import codecs
import csv
import datetime
import gettext
import os
import re
from tornado import escape
from tornado.log import gen_log
from tornado._locale_data import LOCALE_NAMES
from typing import Iterable, Any, Union, Dict
import gettext


def format_date(self, date: Union[(int, float, datetime.datetime)], gmt_offset: int=0, relative: bool=True, shorter: bool=False, full_format: bool=False) -> str:
    'Formats the given date (which should be GMT).\n\n        By default, we return a relative time (e.g., "2 minutes ago"). You\n        can return an absolute date string with ``relative=False``.\n\n        You can force a full format date ("July 10, 1980") with\n        ``full_format=True``.\n\n        This method is primarily intended for dates in the past.\n        For dates in the future, we fall back to full format.\n        '
    if isinstance(date, (int, float)):
        date = datetime.datetime.utcfromtimestamp(date)
    now = datetime.datetime.utcnow()
    if (date > now):
        if (relative and ((date - now).seconds < 60)):
            date = now
        else:
            full_format = True
    local_date = (date - datetime.timedelta(minutes=gmt_offset))
    local_now = (now - datetime.timedelta(minutes=gmt_offset))
    local_yesterday = (local_now - datetime.timedelta(hours=24))
    difference = (now - date)
    seconds = difference.seconds
    days = difference.days
    _ = self.translate
    format = None
    if (not full_format):
        if (relative and (days == 0)):
            if (seconds < 50):
                return (_('1 second ago', '%(seconds)d seconds ago', seconds) % {'seconds': seconds})
            if (seconds < (50 * 60)):
                minutes = round((seconds / 60.0))
                return (_('1 minute ago', '%(minutes)d minutes ago', minutes) % {'minutes': minutes})
            hours = round((seconds / (60.0 * 60)))
            return (_('1 hour ago', '%(hours)d hours ago', hours) % {'hours': hours})
        if (days == 0):
            format = _('%(time)s')
        elif ((days == 1) and (local_date.day == local_yesterday.day) and relative):
            format = (_('yesterday') if shorter else _('yesterday at %(time)s'))
        elif (days < 5):
            format = (_('%(weekday)s') if shorter else _('%(weekday)s at %(time)s'))
        elif (days < 334):
            format = (_('%(month_name)s %(day)s') if shorter else _('%(month_name)s %(day)s at %(time)s'))
    if (format is None):
        format = (_('%(month_name)s %(day)s, %(year)s') if shorter else _('%(month_name)s %(day)s, %(year)s at %(time)s'))
    tfhour_clock = (self.code not in ('en', 'en_US', 'zh_CN'))
    if tfhour_clock:
        str_time = ('%d:%02d' % (local_date.hour, local_date.minute))
    elif (self.code == 'zh_CN'):
        str_time = ('%s%d:%02d' % ((u'上午', u'下午')[(local_date.hour >= 12)], ((local_date.hour % 12) or 12), local_date.minute))
    else:
        str_time = ('%d:%02d %s' % (((local_date.hour % 12) or 12), local_date.minute, ('am', 'pm')[(local_date.hour >= 12)]))
    return (format % {'month_name': self._months[(local_date.month - 1)], 'weekday': self._weekdays[local_date.weekday()], 'day': str(local_date.day), 'year': str(local_date.year), 'time': str_time})
