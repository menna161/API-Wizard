import asyncio
import datetime
import os
import pathlib
import pickle
import re
from collections import defaultdict
from http.cookies import BaseCookie, Morsel, SimpleCookie
from typing import DefaultDict, Dict, Iterable, Iterator, Mapping, Optional, Set, Tuple, Union, cast
from yarl import URL
from .abc import AbstractCookieJar
from .helpers import is_ip_address, next_whole_second
from .typedefs import LooseCookies, PathLike


@classmethod
def _parse_date(cls, date_str: str) -> Optional[datetime.datetime]:
    'Implements date string parsing adhering to RFC 6265.'
    if (not date_str):
        return None
    found_time = False
    found_day = False
    found_month = False
    found_year = False
    hour = minute = second = 0
    day = 0
    month = 0
    year = 0
    for token_match in cls.DATE_TOKENS_RE.finditer(date_str):
        token = token_match.group('token')
        if (not found_time):
            time_match = cls.DATE_HMS_TIME_RE.match(token)
            if time_match:
                found_time = True
                (hour, minute, second) = [int(s) for s in time_match.groups()]
                continue
        if (not found_day):
            day_match = cls.DATE_DAY_OF_MONTH_RE.match(token)
            if day_match:
                found_day = True
                day = int(day_match.group())
                continue
        if (not found_month):
            month_match = cls.DATE_MONTH_RE.match(token)
            if month_match:
                found_month = True
                assert (month_match.lastindex is not None)
                month = month_match.lastindex
                continue
        if (not found_year):
            year_match = cls.DATE_YEAR_RE.match(token)
            if year_match:
                found_year = True
                year = int(year_match.group())
    if (70 <= year <= 99):
        year += 1900
    elif (0 <= year <= 69):
        year += 2000
    if (False in (found_day, found_month, found_year, found_time)):
        return None
    if (not (1 <= day <= 31)):
        return None
    if ((year < 1601) or (hour > 23) or (minute > 59) or (second > 59)):
        return None
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=datetime.timezone.utc)
