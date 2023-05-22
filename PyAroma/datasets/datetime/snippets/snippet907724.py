import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def __init__(self):
    BaseCalendarTest.__init__(self)
    self.holidays = [parse(x) for x in global_holidays.split('\n')]
    self.cal = Calendar(workdays=[0], holidays=self.holidays)
    rr = rruleset()
    rr.rrule(rrule(DAILY, byweekday=MO, dtstart=datetime.datetime(2010, 1, 1)))
    for h in self.holidays:
        rr.exdate(h)
    self.rr = rr
    self.dates = rr.between(datetime.datetime(2010, 1, 1), datetime.datetime(2013, 12, 31), inc=True)
