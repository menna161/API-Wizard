import datetime
import decimal
import re
from typing import Any, Callable, Dict, Iterator, List, Optional, TypeVar, Union, cast
from xml.dom.minidom import Document
from xml.dom.minidom import Element as XmlElement
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from ._utils import StreamType, deprecate_with_replacement, deprecation_with_replacement
from .errors import PdfReadError
from .generic import ContentStream, PdfObject


def _converter_date(value: str) -> datetime.datetime:
    matches = iso8601.match(value)
    if (matches is None):
        raise ValueError(f'Invalid date format: {value}')
    year = int(matches.group('year'))
    month = int((matches.group('month') or '1'))
    day = int((matches.group('day') or '1'))
    hour = int((matches.group('hour') or '0'))
    minute = int((matches.group('minute') or '0'))
    second = decimal.Decimal((matches.group('second') or '0'))
    seconds_dec = second.to_integral(decimal.ROUND_FLOOR)
    milliseconds_dec = ((second - seconds_dec) * 1000000)
    seconds = int(seconds_dec)
    milliseconds = int(milliseconds_dec)
    tzd = (matches.group('tzd') or 'Z')
    dt = datetime.datetime(year, month, day, hour, minute, seconds, milliseconds)
    if (tzd != 'Z'):
        (tzd_hours, tzd_minutes) = (int(x) for x in tzd.split(':'))
        tzd_hours *= (- 1)
        if (tzd_hours < 0):
            tzd_minutes *= (- 1)
        dt = (dt + datetime.timedelta(hours=tzd_hours, minutes=tzd_minutes))
    return dt
