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


def format_day(self, date: datetime.datetime, gmt_offset: int=0, dow: bool=True) -> bool:
    'Formats the given date as a day of week.\n\n        Example: "Monday, January 22". You can remove the day of week with\n        ``dow=False``.\n        '
    local_date = (date - datetime.timedelta(minutes=gmt_offset))
    _ = self.translate
    if dow:
        return (_('%(weekday)s, %(month_name)s %(day)s') % {'month_name': self._months[(local_date.month - 1)], 'weekday': self._weekdays[local_date.weekday()], 'day': str(local_date.day)})
    else:
        return (_('%(month_name)s %(day)s') % {'month_name': self._months[(local_date.month - 1)], 'day': str(local_date.day)})
