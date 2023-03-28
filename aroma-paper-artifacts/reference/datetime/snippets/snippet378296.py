import datetime
import errno
import importlib
import json
import logging
import logging.handlers
import os
import re
from timeit import default_timer as timer


def fromisoformat(date_string):
    '\n    Inspired by: https://docs.python.org/3/library/datetime.html#datetime.date.fromisoformat\n    '
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
