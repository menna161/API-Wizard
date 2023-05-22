from business_calendar import Calendar
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR
from dateutil.parser import parse
import datetime
import timeit


def init_rruleset():
    rr = rruleset()
    rr.rrule(rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=datetime.datetime(2010, 1, 1)))
    for h in holidays:
        rr.exdate(h)
    return rr
