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


def _parse(self, timestr, dayfirst=None, yearfirst=None, fuzzy=False, fuzzy_with_tokens=False):
    '\n        Private method which performs the heavy lifting of parsing, called from\n        ``parse()``, which passes on its ``kwargs`` to this function.\n\n        :param timestr:\n            The string to parse.\n\n        :param dayfirst:\n            Whether to interpret the first value in an ambiguous 3-integer date\n            (e.g. 01/05/09) as the day (``True``) or month (``False``). If\n            ``yearfirst`` is set to ``True``, this distinguishes between YDM\n            and YMD. If set to ``None``, this value is retrieved from the\n            current :class:`parserinfo` object (which itself defaults to\n            ``False``).\n\n        :param yearfirst:\n            Whether to interpret the first value in an ambiguous 3-integer date\n            (e.g. 01/05/09) as the year. If ``True``, the first number is taken\n            to be the year, otherwise the last number is taken to be the year.\n            If this is set to ``None``, the value is retrieved from the current\n            :class:`parserinfo` object (which itself defaults to ``False``).\n\n        :param fuzzy:\n            Whether to allow fuzzy parsing, allowing for string like "Today is\n            January 1, 2047 at 8:21:00AM".\n\n        :param fuzzy_with_tokens:\n            If ``True``, ``fuzzy`` is automatically set to True, and the parser\n            will return a tuple where the first element is the parsed\n            :class:`datetime.datetime` datetimestamp and the second element is\n            a tuple containing the portions of the string which were ignored:\n\n            .. doctest::\n\n                >>> from dateutil.parser import parse\n                >>> parse("Today is January 1, 2047 at 8:21:00AM", fuzzy_with_tokens=True)\n                (datetime.datetime(2047, 1, 1, 8, 21), (u\'Today is \', u\' \', u\'at \'))\n\n        '
    if fuzzy_with_tokens:
        fuzzy = True
    info = self.info
    if (dayfirst is None):
        dayfirst = info.dayfirst
    if (yearfirst is None):
        yearfirst = info.yearfirst
    res = self._result()
    l = _timelex.split(timestr)
    last_skipped_token_i = (- 2)
    skipped_tokens = list()
    try:
        ymd = _ymd(timestr)
        mstridx = (- 1)
        len_l = len(l)
        i = 0
        while (i < len_l):
            try:
                value_repr = l[i]
                value = float(value_repr)
            except ValueError:
                value = None
            if (value is not None):
                len_li = len(l[i])
                i += 1
                if ((len(ymd) == 3) and (len_li in (2, 4)) and (res.hour is None) and ((i >= len_l) or ((l[i] != ':') and (info.hms(l[i]) is None)))):
                    s = l[(i - 1)]
                    res.hour = int(s[:2])
                    if (len_li == 4):
                        res.minute = int(s[2:])
                elif ((len_li == 6) or ((len_li > 6) and (l[(i - 1)].find('.') == 6))):
                    s = l[(i - 1)]
                    if ((not ymd) and (l[(i - 1)].find('.') == (- 1))):
                        ymd.append(s[:2])
                        ymd.append(s[2:4])
                        ymd.append(s[4:])
                    else:
                        res.hour = int(s[:2])
                        res.minute = int(s[2:4])
                        (res.second, res.microsecond) = _parsems(s[4:])
                elif (len_li in (8, 12, 14)):
                    s = l[(i - 1)]
                    ymd.append(s[:4])
                    ymd.append(s[4:6])
                    ymd.append(s[6:8])
                    if (len_li > 8):
                        res.hour = int(s[8:10])
                        res.minute = int(s[10:12])
                        if (len_li > 12):
                            res.second = int(s[12:])
                elif (((i < len_l) and (info.hms(l[i]) is not None)) or (((i + 1) < len_l) and (l[i] == ' ') and (info.hms(l[(i + 1)]) is not None))):
                    if (l[i] == ' '):
                        i += 1
                    idx = info.hms(l[i])
                    while True:
                        if (idx == 0):
                            res.hour = int(value)
                            if (value % 1):
                                res.minute = int((60 * (value % 1)))
                        elif (idx == 1):
                            res.minute = int(value)
                            if (value % 1):
                                res.second = int((60 * (value % 1)))
                        elif (idx == 2):
                            (res.second, res.microsecond) = _parsems(value_repr)
                        i += 1
                        if ((i >= len_l) or (idx == 2)):
                            break
                        try:
                            value_repr = l[i]
                            value = float(value_repr)
                        except ValueError:
                            break
                        else:
                            i += 1
                            idx += 1
                            if (i < len_l):
                                newidx = info.hms(l[i])
                                if (newidx is not None):
                                    idx = newidx
                elif ((i == len_l) and (l[(i - 2)] == ' ') and (info.hms(l[(i - 3)]) is not None)):
                    idx = (info.hms(l[(i - 3)]) + 1)
                    if (idx == 1):
                        res.minute = int(value)
                        if (value % 1):
                            res.second = int((60 * (value % 1)))
                        elif (idx == 2):
                            (res.second, res.microsecond) = _parsems(value_repr)
                            i += 1
                elif (((i + 1) < len_l) and (l[i] == ':')):
                    res.hour = int(value)
                    i += 1
                    value = float(l[i])
                    res.minute = int(value)
                    if (value % 1):
                        res.second = int((60 * (value % 1)))
                    i += 1
                    if ((i < len_l) and (l[i] == ':')):
                        (res.second, res.microsecond) = _parsems(l[(i + 1)])
                        i += 2
                elif ((i < len_l) and (l[i] in ('-', '/', '.'))):
                    sep = l[i]
                    ymd.append(value_repr)
                    i += 1
                    if ((i < len_l) and (not info.jump(l[i]))):
                        try:
                            ymd.append(l[i])
                        except ValueError:
                            value = info.month(l[i])
                            if (value is not None):
                                ymd.append(value)
                                assert (mstridx == (- 1))
                                mstridx = (len(ymd) - 1)
                            else:
                                return (None, None)
                        i += 1
                        if ((i < len_l) and (l[i] == sep)):
                            i += 1
                            value = info.month(l[i])
                            if (value is not None):
                                ymd.append(value)
                                mstridx = (len(ymd) - 1)
                                assert (mstridx == (- 1))
                            else:
                                ymd.append(l[i])
                            i += 1
                elif ((i >= len_l) or info.jump(l[i])):
                    if (((i + 1) < len_l) and (info.ampm(l[(i + 1)]) is not None)):
                        res.hour = int(value)
                        if ((res.hour < 12) and (info.ampm(l[(i + 1)]) == 1)):
                            res.hour += 12
                        elif ((res.hour == 12) and (info.ampm(l[(i + 1)]) == 0)):
                            res.hour = 0
                        i += 1
                    else:
                        ymd.append(value)
                    i += 1
                elif (info.ampm(l[i]) is not None):
                    res.hour = int(value)
                    if ((res.hour < 12) and (info.ampm(l[i]) == 1)):
                        res.hour += 12
                    elif ((res.hour == 12) and (info.ampm(l[i]) == 0)):
                        res.hour = 0
                    i += 1
                elif (not fuzzy):
                    return (None, None)
                else:
                    i += 1
                continue
            value = info.weekday(l[i])
            if (value is not None):
                res.weekday = value
                i += 1
                continue
            value = info.month(l[i])
            if (value is not None):
                ymd.append(value)
                assert (mstridx == (- 1))
                mstridx = (len(ymd) - 1)
                i += 1
                if (i < len_l):
                    if (l[i] in ('-', '/')):
                        sep = l[i]
                        i += 1
                        ymd.append(l[i])
                        i += 1
                        if ((i < len_l) and (l[i] == sep)):
                            i += 1
                            ymd.append(l[i])
                            i += 1
                    elif (((i + 3) < len_l) and (l[i] == l[(i + 2)] == ' ') and info.pertain(l[(i + 1)])):
                        try:
                            value = int(l[(i + 3)])
                        except ValueError:
                            pass
                        else:
                            ymd.append(str(info.convertyear(value)))
                        i += 4
                continue
            value = info.ampm(l[i])
            if (value is not None):
                val_is_ampm = True
                if (fuzzy and (res.ampm is not None)):
                    val_is_ampm = False
                if (res.hour is None):
                    if fuzzy:
                        val_is_ampm = False
                    else:
                        raise ValueError(('No hour specified with ' + 'AM or PM flag.'))
                elif (not (0 <= res.hour <= 12)):
                    if fuzzy:
                        val_is_ampm = False
                    else:
                        raise ValueError(('Invalid hour specified for ' + '12-hour clock.'))
                if val_is_ampm:
                    if ((value == 1) and (res.hour < 12)):
                        res.hour += 12
                    elif ((value == 0) and (res.hour == 12)):
                        res.hour = 0
                    res.ampm = value
                i += 1
                continue
            if ((res.hour is not None) and (len(l[i]) <= 5) and (res.tzname is None) and (res.tzoffset is None) and (not [x for x in l[i] if (x not in string.ascii_uppercase)])):
                res.tzname = l[i]
                res.tzoffset = info.tzoffset(res.tzname)
                i += 1
                if ((i < len_l) and (l[i] in ('+', '-'))):
                    l[i] = ('+', '-')[(l[i] == '+')]
                    res.tzoffset = None
                    if info.utczone(res.tzname):
                        res.tzname = None
                continue
            if ((res.hour is not None) and (l[i] in ('+', '-'))):
                signal = ((- 1), 1)[(l[i] == '+')]
                i += 1
                len_li = len(l[i])
                if (len_li == 4):
                    res.tzoffset = ((int(l[i][:2]) * 3600) + (int(l[i][2:]) * 60))
                elif (((i + 1) < len_l) and (l[(i + 1)] == ':')):
                    res.tzoffset = ((int(l[i]) * 3600) + (int(l[(i + 2)]) * 60))
                    i += 2
                elif (len_li <= 2):
                    res.tzoffset = (int(l[i][:2]) * 3600)
                else:
                    return (None, None)
                i += 1
                res.tzoffset *= signal
                if (((i + 3) < len_l) and info.jump(l[i]) and (l[(i + 1)] == '(') and (l[(i + 3)] == ')') and (3 <= len(l[(i + 2)]) <= 5) and (not [x for x in l[(i + 2)] if (x not in string.ascii_uppercase)])):
                    res.tzname = l[(i + 2)]
                    i += 4
                continue
            if (not (info.jump(l[i]) or fuzzy)):
                return (None, None)
            if (last_skipped_token_i == (i - 1)):
                skipped_tokens[(- 1)] += l[i]
            else:
                skipped_tokens.append(l[i])
            last_skipped_token_i = i
            i += 1
        (year, month, day) = ymd.resolve_ymd(mstridx, yearfirst, dayfirst)
        if (year is not None):
            res.year = year
            res.century_specified = ymd.century_specified
        if (month is not None):
            res.month = month
        if (day is not None):
            res.day = day
    except (IndexError, ValueError, AssertionError):
        return (None, None)
    if (not info.validate(res)):
        return (None, None)
    if fuzzy_with_tokens:
        return (res, tuple(skipped_tokens))
    else:
        return (res, None)
