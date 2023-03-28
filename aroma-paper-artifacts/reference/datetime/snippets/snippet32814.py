from __future__ import unicode_literals
import datetime
import string
import time
import collections
import re
from io import StringIO
from calendar import monthrange, isleap
from six import text_type, binary_type, integer_types
from . import relativedelta
from . import tz


def parse(self, timestr, default=None, ignoretz=False, tzinfos=None, **kwargs):
    '\n        Parse the date/time string into a :class:`datetime.datetime` object.\n\n        :param timestr:\n            Any date/time string using the supported formats.\n\n        :param default:\n            The default datetime object, if this is a datetime object and not\n            ``None``, elements specified in ``timestr`` replace elements in the\n            default object.\n\n        :param ignoretz:\n            If set ``True``, time zones in parsed strings are ignored and a\n            naive :class:`datetime.datetime` object is returned.\n\n        :param tzinfos:\n            Additional time zone names / aliases which may be present in the\n            string. This argument maps time zone names (and optionally offsets\n            from those time zones) to time zones. This parameter can be a\n            dictionary with timezone aliases mapping time zone names to time\n            zones or a function taking two parameters (``tzname`` and\n            ``tzoffset``) and returning a time zone.\n\n            The timezones to which the names are mapped can be an integer\n            offset from UTC in minutes or a :class:`tzinfo` object.\n\n            .. doctest::\n               :options: +NORMALIZE_WHITESPACE\n\n                >>> from dateutil.parser import parse\n                >>> from dateutil.tz import gettz\n                >>> tzinfos = {"BRST": -10800, "CST": gettz("America/Chicago")}\n                >>> parse("2012-01-19 17:21:00 BRST", tzinfos=tzinfos)\n                datetime.datetime(2012, 1, 19, 17, 21, tzinfo=tzoffset(u\'BRST\', -10800))\n                >>> parse("2012-01-19 17:21:00 CST", tzinfos=tzinfos)\n                datetime.datetime(2012, 1, 19, 17, 21,\n                                  tzinfo=tzfile(\'/usr/share/zoneinfo/America/Chicago\'))\n\n            This parameter is ignored if ``ignoretz`` is set.\n\n        :param **kwargs:\n            Keyword arguments as passed to ``_parse()``.\n\n        :return:\n            Returns a :class:`datetime.datetime` object or, if the\n            ``fuzzy_with_tokens`` option is ``True``, returns a tuple, the\n            first element being a :class:`datetime.datetime` object, the second\n            a tuple containing the fuzzy tokens.\n\n        :raises ValueError:\n            Raised for invalid or unknown string format, if the provided\n            :class:`tzinfo` is not in a valid format, or if an invalid date\n            would be created.\n\n        :raises OverflowError:\n            Raised if the parsed date exceeds the largest valid C integer on\n            your system.\n        '
    if (default is None):
        effective_dt = datetime.datetime.now()
        default = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        effective_dt = default
    (res, skipped_tokens) = self._parse(timestr, **kwargs)
    if (res is None):
        raise ValueError('Unknown string format')
    if (len(res) == 0):
        raise ValueError('String does not contain a date.')
    repl = {}
    for attr in ('year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'):
        value = getattr(res, attr)
        if (value is not None):
            repl[attr] = value
    if ('day' not in repl):
        cyear = (default.year if (res.year is None) else res.year)
        cmonth = (default.month if (res.month is None) else res.month)
        cday = (default.day if (res.day is None) else res.day)
        if (cday > monthrange(cyear, cmonth)[1]):
            repl['day'] = monthrange(cyear, cmonth)[1]
    ret = default.replace(**repl)
    if ((res.weekday is not None) and (not res.day)):
        ret = (ret + relativedelta.relativedelta(weekday=res.weekday))
    if (not ignoretz):
        if (isinstance(tzinfos, collections.Callable) or (tzinfos and (res.tzname in tzinfos))):
            if isinstance(tzinfos, collections.Callable):
                tzdata = tzinfos(res.tzname, res.tzoffset)
            else:
                tzdata = tzinfos.get(res.tzname)
            if isinstance(tzdata, datetime.tzinfo):
                tzinfo = tzdata
            elif isinstance(tzdata, text_type):
                tzinfo = tz.tzstr(tzdata)
            elif isinstance(tzdata, integer_types):
                tzinfo = tz.tzoffset(res.tzname, tzdata)
            else:
                raise ValueError('Offset must be tzinfo subclass, tz string, or int offset.')
            ret = ret.replace(tzinfo=tzinfo)
        elif (res.tzname and (res.tzname in time.tzname)):
            ret = ret.replace(tzinfo=tz.tzlocal())
        elif (res.tzoffset == 0):
            ret = ret.replace(tzinfo=tz.tzutc())
        elif res.tzoffset:
            ret = ret.replace(tzinfo=tz.tzoffset(res.tzname, res.tzoffset))
    if kwargs.get('fuzzy_with_tokens', False):
        return (ret, skipped_tokens)
    else:
        return ret
