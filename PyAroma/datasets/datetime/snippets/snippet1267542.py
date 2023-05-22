import sys
import datetime
import os.path
from pytz.exceptions import AmbiguousTimeError
from pytz.exceptions import InvalidTimeError
from pytz.exceptions import NonExistentTimeError
from pytz.exceptions import UnknownTimeZoneError
from pytz.lazy import LazyDict, LazyList, LazySet
from pytz.tzinfo import unpickler, BaseTzInfo
from pytz.tzfile import build_tzinfo
import doctest
import pytz
from pkg_resources import resource_stream


def timezone(zone):
    " Return a datetime.tzinfo implementation for the given timezone\n\n    >>> from datetime import datetime, timedelta\n    >>> utc = timezone('UTC')\n    >>> eastern = timezone('US/Eastern')\n    >>> eastern.zone\n    'US/Eastern'\n    >>> timezone(unicode('US/Eastern')) is eastern\n    True\n    >>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)\n    >>> loc_dt = utc_dt.astimezone(eastern)\n    >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'\n    >>> loc_dt.strftime(fmt)\n    '2002-10-27 01:00:00 EST (-0500)'\n    >>> (loc_dt - timedelta(minutes=10)).strftime(fmt)\n    '2002-10-27 00:50:00 EST (-0500)'\n    >>> eastern.normalize(loc_dt - timedelta(minutes=10)).strftime(fmt)\n    '2002-10-27 01:50:00 EDT (-0400)'\n    >>> (loc_dt + timedelta(minutes=10)).strftime(fmt)\n    '2002-10-27 01:10:00 EST (-0500)'\n\n    Raises UnknownTimeZoneError if passed an unknown zone.\n\n    >>> try:\n    ...     timezone('Asia/Shangri-La')\n    ... except UnknownTimeZoneError:\n    ...     print('Unknown')\n    Unknown\n\n    >>> try:\n    ...     timezone(unicode('\\N{TRADE MARK SIGN}'))\n    ... except UnknownTimeZoneError:\n    ...     print('Unknown')\n    Unknown\n\n    "
    if (zone.upper() == 'UTC'):
        return utc
    try:
        zone = ascii(zone)
    except UnicodeEncodeError:
        raise UnknownTimeZoneError(zone)
    zone = _unmunge_zone(zone)
    if (zone not in _tzinfo_cache):
        if (zone in all_timezones_set):
            fp = open_resource(zone)
            try:
                _tzinfo_cache[zone] = build_tzinfo(zone, fp)
            finally:
                fp.close()
        else:
            raise UnknownTimeZoneError(zone)
    return _tzinfo_cache[zone]
