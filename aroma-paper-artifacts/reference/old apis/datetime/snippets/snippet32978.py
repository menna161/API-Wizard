import itertools
import datetime
import calendar
import sys
from six import advance_iterator, integer_types
from six.moves import _thread
import heapq
from warnings import warn
from math import gcd
from fractions import gcd
from dateutil import parser
from dateutil import easter
from dateutil import parser
from dateutil import parser


def __init__(self, freq, dtstart=None, interval=1, wkst=None, count=None, until=None, bysetpos=None, bymonth=None, bymonthday=None, byyearday=None, byeaster=None, byweekno=None, byweekday=None, byhour=None, byminute=None, bysecond=None, cache=False):
    super(rrule, self).__init__(cache)
    global easter
    if (not dtstart):
        dtstart = datetime.datetime.now().replace(microsecond=0)
    elif (not isinstance(dtstart, datetime.datetime)):
        dtstart = datetime.datetime.fromordinal(dtstart.toordinal())
    else:
        dtstart = dtstart.replace(microsecond=0)
    self._dtstart = dtstart
    self._tzinfo = dtstart.tzinfo
    self._freq = freq
    self._interval = interval
    self._count = count
    self._original_rule = {}
    if (until and (not isinstance(until, datetime.datetime))):
        until = datetime.datetime.fromordinal(until.toordinal())
    self._until = until
    if (count and until):
        warn("Using both 'count' and 'until' is inconsistent with RFC 2445 and has been deprecated in dateutil. Future versions will raise an error.", DeprecationWarning)
    if (wkst is None):
        self._wkst = calendar.firstweekday()
    elif isinstance(wkst, integer_types):
        self._wkst = wkst
    else:
        self._wkst = wkst.weekday
    if (bysetpos is None):
        self._bysetpos = None
    elif isinstance(bysetpos, integer_types):
        if ((bysetpos == 0) or (not ((- 366) <= bysetpos <= 366))):
            raise ValueError('bysetpos must be between 1 and 366, or between -366 and -1')
        self._bysetpos = (bysetpos,)
    else:
        self._bysetpos = tuple(bysetpos)
        for pos in self._bysetpos:
            if ((pos == 0) or (not ((- 366) <= pos <= 366))):
                raise ValueError('bysetpos must be between 1 and 366, or between -366 and -1')
    if self._bysetpos:
        self._original_rule['bysetpos'] = self._bysetpos
    if ((byweekno is None) and (byyearday is None) and (bymonthday is None) and (byweekday is None) and (byeaster is None)):
        if (freq == YEARLY):
            if (bymonth is None):
                bymonth = dtstart.month
                self._original_rule['bymonth'] = None
            bymonthday = dtstart.day
            self._original_rule['bymonthday'] = None
        elif (freq == MONTHLY):
            bymonthday = dtstart.day
            self._original_rule['bymonthday'] = None
        elif (freq == WEEKLY):
            byweekday = dtstart.weekday()
            self._original_rule['byweekday'] = None
    if (bymonth is None):
        self._bymonth = None
    else:
        if isinstance(bymonth, integer_types):
            bymonth = (bymonth,)
        self._bymonth = tuple(sorted(set(bymonth)))
        if ('bymonth' not in self._original_rule):
            self._original_rule['bymonth'] = self._bymonth
    if (byyearday is None):
        self._byyearday = None
    else:
        if isinstance(byyearday, integer_types):
            byyearday = (byyearday,)
        self._byyearday = tuple(sorted(set(byyearday)))
        self._original_rule['byyearday'] = self._byyearday
    if (byeaster is not None):
        if (not easter):
            from dateutil import easter
        if isinstance(byeaster, integer_types):
            self._byeaster = (byeaster,)
        else:
            self._byeaster = tuple(sorted(byeaster))
        self._original_rule['byeaster'] = self._byeaster
    else:
        self._byeaster = None
    if (bymonthday is None):
        self._bymonthday = ()
        self._bynmonthday = ()
    else:
        if isinstance(bymonthday, integer_types):
            bymonthday = (bymonthday,)
        bymonthday = set(bymonthday)
        self._bymonthday = tuple(sorted([x for x in bymonthday if (x > 0)]))
        self._bynmonthday = tuple(sorted([x for x in bymonthday if (x < 0)]))
        if ('bymonthday' not in self._original_rule):
            self._original_rule['bymonthday'] = tuple(itertools.chain(self._bymonthday, self._bynmonthday))
    if (byweekno is None):
        self._byweekno = None
    else:
        if isinstance(byweekno, integer_types):
            byweekno = (byweekno,)
        self._byweekno = tuple(sorted(set(byweekno)))
        self._original_rule['byweekno'] = self._byweekno
    if (byweekday is None):
        self._byweekday = None
        self._bynweekday = None
    else:
        if (isinstance(byweekday, integer_types) or hasattr(byweekday, 'n')):
            byweekday = (byweekday,)
        self._byweekday = set()
        self._bynweekday = set()
        for wday in byweekday:
            if isinstance(wday, integer_types):
                self._byweekday.add(wday)
            elif ((not wday.n) or (freq > MONTHLY)):
                self._byweekday.add(wday.weekday)
            else:
                self._bynweekday.add((wday.weekday, wday.n))
        if (not self._byweekday):
            self._byweekday = None
        elif (not self._bynweekday):
            self._bynweekday = None
        if (self._byweekday is not None):
            self._byweekday = tuple(sorted(self._byweekday))
            orig_byweekday = [weekday(x) for x in self._byweekday]
        else:
            orig_byweekday = tuple()
        if (self._bynweekday is not None):
            self._bynweekday = tuple(sorted(self._bynweekday))
            orig_bynweekday = [weekday(*x) for x in self._bynweekday]
        else:
            orig_bynweekday = tuple()
        if ('byweekday' not in self._original_rule):
            self._original_rule['byweekday'] = tuple(itertools.chain(orig_byweekday, orig_bynweekday))
    if (byhour is None):
        if (freq < HOURLY):
            self._byhour = set((dtstart.hour,))
        else:
            self._byhour = None
    else:
        if isinstance(byhour, integer_types):
            byhour = (byhour,)
        if (freq == HOURLY):
            self._byhour = self.__construct_byset(start=dtstart.hour, byxxx=byhour, base=24)
        else:
            self._byhour = set(byhour)
        self._byhour = tuple(sorted(self._byhour))
        self._original_rule['byhour'] = self._byhour
    if (byminute is None):
        if (freq < MINUTELY):
            self._byminute = set((dtstart.minute,))
        else:
            self._byminute = None
    else:
        if isinstance(byminute, integer_types):
            byminute = (byminute,)
        if (freq == MINUTELY):
            self._byminute = self.__construct_byset(start=dtstart.minute, byxxx=byminute, base=60)
        else:
            self._byminute = set(byminute)
        self._byminute = tuple(sorted(self._byminute))
        self._original_rule['byminute'] = self._byminute
    if (bysecond is None):
        if (freq < SECONDLY):
            self._bysecond = (dtstart.second,)
        else:
            self._bysecond = None
    else:
        if isinstance(bysecond, integer_types):
            bysecond = (bysecond,)
        self._bysecond = set(bysecond)
        if (freq == SECONDLY):
            self._bysecond = self.__construct_byset(start=dtstart.second, byxxx=bysecond, base=60)
        else:
            self._bysecond = set(bysecond)
        self._bysecond = tuple(sorted(self._bysecond))
        self._original_rule['bysecond'] = self._bysecond
    if (self._freq >= HOURLY):
        self._timeset = None
    else:
        self._timeset = []
        for hour in self._byhour:
            for minute in self._byminute:
                for second in self._bysecond:
                    self._timeset.append(datetime.time(hour, minute, second, tzinfo=self._tzinfo))
        self._timeset.sort()
        self._timeset = tuple(self._timeset)
