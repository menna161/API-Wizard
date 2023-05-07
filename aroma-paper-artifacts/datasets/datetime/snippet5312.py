import datetime
import os
import re
from pathlib import Path
from stat import ST_CTIME, ST_MTIME, ST_SIZE
from typing import Generator
from saucenao.files.constraint import Constraint


@staticmethod
def _get_timestamp_from_datestring(date_string) -> float:
    'Convert the given date string to timestamp\n\n        :param date_string:\n        :return:\n        '
    if re.match('\\d+.\\d+.\\d+ \\d+:\\d+:\\d+', date_string):
        return datetime.datetime.strptime(date_string, '%d.%m.%Y %H:%M:%S').timestamp()
    elif re.match('\\d+.\\d+.\\d+ \\d+:\\d+', date_string):
        return datetime.datetime.strptime(date_string, '%d.%m.%Y %H:%M').timestamp()
    elif re.match('\\d+.\\d+.\\d+', date_string):
        return datetime.datetime.strptime(date_string, '%d.%m.%Y').timestamp()
    else:
        raise AttributeError("The date doesn't fit the format: d.m.Y[ H:M[:S]]")
