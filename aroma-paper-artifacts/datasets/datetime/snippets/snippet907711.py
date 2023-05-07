import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def test_eom(self):
    print('test_eom')
    err_count = 0
    for i in range(1, len(self.dates)):
        if (self.dates[i].month != self.dates[(i - 1)].month):
            date = (self.dates[(i - 1)] - datetime.timedelta(days=10))
            calc_date = self.cal.buseom(date)
            if (self.dates[(i - 1)] != calc_date):
                print(('Error [%s-%s] got %s expected %s' % (self.dates[(i - 1)].year, self.dates[(i - 1)].month, calc_date, self.dates[(i - 1)])))
                err_count += 1
        if (err_count > 10):
            break
    assert (err_count == 0)
