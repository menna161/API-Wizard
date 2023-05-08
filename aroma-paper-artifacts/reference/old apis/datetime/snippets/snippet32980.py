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


def _iter(self):
    (year, month, day, hour, minute, second, weekday, yearday, _) = self._dtstart.timetuple()
    freq = self._freq
    interval = self._interval
    wkst = self._wkst
    until = self._until
    bymonth = self._bymonth
    byweekno = self._byweekno
    byyearday = self._byyearday
    byweekday = self._byweekday
    byeaster = self._byeaster
    bymonthday = self._bymonthday
    bynmonthday = self._bynmonthday
    bysetpos = self._bysetpos
    byhour = self._byhour
    byminute = self._byminute
    bysecond = self._bysecond
    ii = _iterinfo(self)
    ii.rebuild(year, month)
    getdayset = {YEARLY: ii.ydayset, MONTHLY: ii.mdayset, WEEKLY: ii.wdayset, DAILY: ii.ddayset, HOURLY: ii.ddayset, MINUTELY: ii.ddayset, SECONDLY: ii.ddayset}[freq]
    if (freq < HOURLY):
        timeset = self._timeset
    else:
        gettimeset = {HOURLY: ii.htimeset, MINUTELY: ii.mtimeset, SECONDLY: ii.stimeset}[freq]
        if (((freq >= HOURLY) and self._byhour and (hour not in self._byhour)) or ((freq >= MINUTELY) and self._byminute and (minute not in self._byminute)) or ((freq >= SECONDLY) and self._bysecond and (second not in self._bysecond))):
            timeset = ()
        else:
            timeset = gettimeset(hour, minute, second)
    total = 0
    count = self._count
    while True:
        (dayset, start, end) = getdayset(year, month, day)
        filtered = False
        for i in dayset[start:end]:
            if ((bymonth and (ii.mmask[i] not in bymonth)) or (byweekno and (not ii.wnomask[i])) or (byweekday and (ii.wdaymask[i] not in byweekday)) or (ii.nwdaymask and (not ii.nwdaymask[i])) or (byeaster and (not ii.eastermask[i])) or ((bymonthday or bynmonthday) and (ii.mdaymask[i] not in bymonthday) and (ii.nmdaymask[i] not in bynmonthday)) or (byyearday and (((i < ii.yearlen) and ((i + 1) not in byyearday) and (((- ii.yearlen) + i) not in byyearday)) or ((i >= ii.yearlen) and (((i + 1) - ii.yearlen) not in byyearday) and ((((- ii.nextyearlen) + i) - ii.yearlen) not in byyearday))))):
                dayset[i] = None
                filtered = True
        if (bysetpos and timeset):
            poslist = []
            for pos in bysetpos:
                if (pos < 0):
                    (daypos, timepos) = divmod(pos, len(timeset))
                else:
                    (daypos, timepos) = divmod((pos - 1), len(timeset))
                try:
                    i = [x for x in dayset[start:end] if (x is not None)][daypos]
                    time = timeset[timepos]
                except IndexError:
                    pass
                else:
                    date = datetime.date.fromordinal((ii.yearordinal + i))
                    res = datetime.datetime.combine(date, time)
                    if (res not in poslist):
                        poslist.append(res)
            poslist.sort()
            for res in poslist:
                if (until and (res > until)):
                    self._len = total
                    return
                elif (res >= self._dtstart):
                    total += 1
                    (yield res)
                    if count:
                        count -= 1
                        if (not count):
                            self._len = total
                            return
        else:
            for i in dayset[start:end]:
                if (i is not None):
                    date = datetime.date.fromordinal((ii.yearordinal + i))
                    for time in timeset:
                        res = datetime.datetime.combine(date, time)
                        if (until and (res > until)):
                            self._len = total
                            return
                        elif (res >= self._dtstart):
                            total += 1
                            (yield res)
                            if count:
                                count -= 1
                                if (not count):
                                    self._len = total
                                    return
        fixday = False
        if (freq == YEARLY):
            year += interval
            if (year > datetime.MAXYEAR):
                self._len = total
                return
            ii.rebuild(year, month)
        elif (freq == MONTHLY):
            month += interval
            if (month > 12):
                (div, mod) = divmod(month, 12)
                month = mod
                year += div
                if (month == 0):
                    month = 12
                    year -= 1
                if (year > datetime.MAXYEAR):
                    self._len = total
                    return
            ii.rebuild(year, month)
        elif (freq == WEEKLY):
            if (wkst > weekday):
                day += ((- ((weekday + 1) + (6 - wkst))) + (self._interval * 7))
            else:
                day += ((- (weekday - wkst)) + (self._interval * 7))
            weekday = wkst
            fixday = True
        elif (freq == DAILY):
            day += interval
            fixday = True
        elif (freq == HOURLY):
            if filtered:
                hour += (((23 - hour) // interval) * interval)
            if byhour:
                (ndays, hour) = self.__mod_distance(value=hour, byxxx=self._byhour, base=24)
            else:
                (ndays, hour) = divmod((hour + interval), 24)
            if ndays:
                day += ndays
                fixday = True
            timeset = gettimeset(hour, minute, second)
        elif (freq == MINUTELY):
            if filtered:
                minute += (((1439 - ((hour * 60) + minute)) // interval) * interval)
            valid = False
            rep_rate = (24 * 60)
            for j in range((rep_rate // gcd(interval, rep_rate))):
                if byminute:
                    (nhours, minute) = self.__mod_distance(value=minute, byxxx=self._byminute, base=60)
                else:
                    (nhours, minute) = divmod((minute + interval), 60)
                (div, hour) = divmod((hour + nhours), 24)
                if div:
                    day += div
                    fixday = True
                    filtered = False
                if ((not byhour) or (hour in byhour)):
                    valid = True
                    break
            if (not valid):
                raise ValueError(('Invalid combination of interval and ' + 'byhour resulting in empty rule.'))
            timeset = gettimeset(hour, minute, second)
        elif (freq == SECONDLY):
            if filtered:
                second += (((86399 - (((hour * 3600) + (minute * 60)) + second)) // interval) * interval)
            rep_rate = (24 * 3600)
            valid = False
            for j in range(0, (rep_rate // gcd(interval, rep_rate))):
                if bysecond:
                    (nminutes, second) = self.__mod_distance(value=second, byxxx=self._bysecond, base=60)
                else:
                    (nminutes, second) = divmod((second + interval), 60)
                (div, minute) = divmod((minute + nminutes), 60)
                if div:
                    hour += div
                    (div, hour) = divmod(hour, 24)
                    if div:
                        day += div
                        fixday = True
                if (((not byhour) or (hour in byhour)) and ((not byminute) or (minute in byminute)) and ((not bysecond) or (second in bysecond))):
                    valid = True
                    break
            if (not valid):
                raise ValueError((('Invalid combination of interval, ' + 'byhour and byminute resulting in empty') + ' rule.'))
            timeset = gettimeset(hour, minute, second)
        if (fixday and (day > 28)):
            daysinmonth = calendar.monthrange(year, month)[1]
            if (day > daysinmonth):
                while (day > daysinmonth):
                    day -= daysinmonth
                    month += 1
                    if (month == 13):
                        month = 1
                        year += 1
                        if (year > datetime.MAXYEAR):
                            self._len = total
                            return
                    daysinmonth = calendar.monthrange(year, month)[1]
                ii.rebuild(year, month)
