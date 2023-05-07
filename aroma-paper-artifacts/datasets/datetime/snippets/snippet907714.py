import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def __init__(self):
    BaseCalendarTest.__init__(self)
    self.cal = Calendar()
    rr = rruleset()
    rr.rrule(rrule(DAILY, byweekday=(MO, TU, WE, TH, FR), dtstart=datetime.datetime(2010, 1, 1)))
    self.rr = rr
    self.dates = rr.between(datetime.datetime(2010, 1, 1), datetime.datetime(2013, 12, 31), inc=True)
