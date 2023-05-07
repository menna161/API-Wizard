import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def test_isbusday(self):
    print('test_isbusday')
    err_count = 0
    for i in range(len(self.dates)):
        date = self.dates[i]
        if (not self.cal.isbusday(date)):
            print(('Error [%s] should be a business day' % date))
            err_count += 1
        if (i > 0):
            d = (date - self.dates[(i - 1)]).days
            while (d > 1):
                date -= datetime.timedelta(days=1)
                if self.cal.isbusday(date):
                    print(('Error [%s] should NOT be a business day' % date))
                    err_count += 1
                d -= 1
        if (err_count > 10):
            break
    assert (err_count == 0)
