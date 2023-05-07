import types
import typing as T
import collections
import datetime
import re
import voluptuous as vol


def format_time(when: datetime.time, format_str: str=TIME_FORMAT) -> str:
    'Returns a string representing the given datetime.time object.\n    If no strftime-compatible format is provided, the default is used.'
    return when.strftime(format_str)
