import types
import typing as T
import collections
import datetime
import re
import voluptuous as vol


def parse_time_string(time_str: str) -> datetime.time:
    'Parses a string recognizable by TIME_REGEXP into a datetime.time object. If\n    the string has an invalid format, a ValueError is raised.'
    match = TIME_REGEXP.match(time_str)
    if (match is None):
        raise ValueError('time string {} has an invalid format'.format(repr(time_str)))
    groups = match.groupdict()
    return datetime.time(int(groups['h']), int(groups['m']), int((groups['s'] or 0)))
