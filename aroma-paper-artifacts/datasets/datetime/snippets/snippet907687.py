from business_calendar import Calendar
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR
from dateutil.parser import parse
import datetime
import timeit


def gen_rruleset_1():
    rr.between(datetime.datetime(2010, 1, 1), datetime.datetime(2013, 12, 31), inc=True)
