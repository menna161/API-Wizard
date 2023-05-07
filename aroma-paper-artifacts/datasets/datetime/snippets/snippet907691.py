from business_calendar import Calendar
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR
from dateutil.parser import parse
import datetime
import timeit


def gen_calendar_3():
    cal.range(datetime.datetime(1970, 1, 1), datetime.datetime(2030, 12, 31))
