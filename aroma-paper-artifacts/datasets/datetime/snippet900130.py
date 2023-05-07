import datetime
import re
import typing
from aiogram import types


def parse_timedelta(value: str) -> datetime.timedelta:
    match = LINE_PATTERN.match(value)
    if (not match):
        raise TimedeltaParseError('Invalid time format')
    try:
        result = datetime.timedelta()
        for match in PATTERN.finditer(value):
            (value, modifier) = match.groups()
            result += (int(value) * MODIFIERS[modifier])
    except OverflowError:
        raise TimedeltaParseError('Timedelta value is too large')
    return result
