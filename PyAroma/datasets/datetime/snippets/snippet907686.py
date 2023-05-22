from business_calendar import Calendar
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR
from dateutil.parser import parse
import datetime
import timeit


def gen_busdaycount_1():
    cal.busdaycount(datetime.datetime(2009, 12, 31), datetime.datetime(2013, 12, 31))
