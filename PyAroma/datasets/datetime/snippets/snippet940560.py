import types
import typing as T
import collections
import datetime
import re
import voluptuous as vol


def parse_rule_time_string(time_str: str) -> T.Tuple[(T.Optional[datetime.time], T.Optional[int])]:
    'Parses a string recognizable by RULE_TIME_REGEXP into a (datetime.time,\n    int) tuple. Both time and days are optional and None if not specified. If the\n    string has an invalid format, a ValueError is raised.'
    match = RULE_TIME_REGEXP.match(time_str)
    if (match is None):
        raise ValueError('time string {} has invalid format'.format(repr(time_str)))
    groups = match.groupdict()
    _time = None
    if groups['time']:
        _time = datetime.time(int(groups['h']), int(groups['m']), int((groups['s'] or 0)))
    days = (None if (groups['days'] is None) else int(groups['days']))
    return (_time, days)
