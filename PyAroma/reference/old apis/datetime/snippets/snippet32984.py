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


def rebuild(self, year, month):
    rr = self.rrule
    if (year != self.lastyear):
        self.yearlen = (365 + calendar.isleap(year))
        self.nextyearlen = (365 + calendar.isleap((year + 1)))
        firstyday = datetime.date(year, 1, 1)
        self.yearordinal = firstyday.toordinal()
        self.yearweekday = firstyday.weekday()
        wday = datetime.date(year, 1, 1).weekday()
        if (self.yearlen == 365):
            self.mmask = M365MASK
            self.mdaymask = MDAY365MASK
            self.nmdaymask = NMDAY365MASK
            self.wdaymask = WDAYMASK[wday:]
            self.mrange = M365RANGE
        else:
            self.mmask = M366MASK
            self.mdaymask = MDAY366MASK
            self.nmdaymask = NMDAY366MASK
            self.wdaymask = WDAYMASK[wday:]
            self.mrange = M366RANGE
        if (not rr._byweekno):
            self.wnomask = None
        else:
            self.wnomask = ([0] * (self.yearlen + 7))
            no1wkst = firstwkst = (((7 - self.yearweekday) + rr._wkst) % 7)
            if (no1wkst >= 4):
                no1wkst = 0
                wyearlen = (self.yearlen + ((self.yearweekday - rr._wkst) % 7))
            else:
                wyearlen = (self.yearlen - no1wkst)
            (div, mod) = divmod(wyearlen, 7)
            numweeks = (div + (mod // 4))
            for n in rr._byweekno:
                if (n < 0):
                    n += (numweeks + 1)
                if (not (0 < n <= numweeks)):
                    continue
                if (n > 1):
                    i = (no1wkst + ((n - 1) * 7))
                    if (no1wkst != firstwkst):
                        i -= (7 - firstwkst)
                else:
                    i = no1wkst
                for j in range(7):
                    self.wnomask[i] = 1
                    i += 1
                    if (self.wdaymask[i] == rr._wkst):
                        break
            if (1 in rr._byweekno):
                i = (no1wkst + (numweeks * 7))
                if (no1wkst != firstwkst):
                    i -= (7 - firstwkst)
                if (i < self.yearlen):
                    for j in range(7):
                        self.wnomask[i] = 1
                        i += 1
                        if (self.wdaymask[i] == rr._wkst):
                            break
            if no1wkst:
                if ((- 1) not in rr._byweekno):
                    lyearweekday = datetime.date((year - 1), 1, 1).weekday()
                    lno1wkst = (((7 - lyearweekday) + rr._wkst) % 7)
                    lyearlen = (365 + calendar.isleap((year - 1)))
                    if (lno1wkst >= 4):
                        lno1wkst = 0
                        lnumweeks = (52 + (((lyearlen + ((lyearweekday - rr._wkst) % 7)) % 7) // 4))
                    else:
                        lnumweeks = (52 + (((self.yearlen - no1wkst) % 7) // 4))
                else:
                    lnumweeks = (- 1)
                if (lnumweeks in rr._byweekno):
                    for i in range(no1wkst):
                        self.wnomask[i] = 1
    if (rr._bynweekday and ((month != self.lastmonth) or (year != self.lastyear))):
        ranges = []
        if (rr._freq == YEARLY):
            if rr._bymonth:
                for month in rr._bymonth:
                    ranges.append(self.mrange[(month - 1):(month + 1)])
            else:
                ranges = [(0, self.yearlen)]
        elif (rr._freq == MONTHLY):
            ranges = [self.mrange[(month - 1):(month + 1)]]
        if ranges:
            self.nwdaymask = ([0] * self.yearlen)
            for (first, last) in ranges:
                last -= 1
                for (wday, n) in rr._bynweekday:
                    if (n < 0):
                        i = (last + ((n + 1) * 7))
                        i -= ((self.wdaymask[i] - wday) % 7)
                    else:
                        i = (first + ((n - 1) * 7))
                        i += (((7 - self.wdaymask[i]) + wday) % 7)
                    if (first <= i <= last):
                        self.nwdaymask[i] = 1
    if rr._byeaster:
        self.eastermask = ([0] * (self.yearlen + 7))
        eyday = (easter.easter(year).toordinal() - self.yearordinal)
        for offset in rr._byeaster:
            self.eastermask[(eyday + offset)] = 1
    self.lastyear = year
    self.lastmonth = month
