import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def test_adjust_modifiedfollowing(self):
    print('test_adjust_modifiedfollowing')
    err_count = 0
    i = (- 1)
    date = self.dates[0]
    while (date <= self.dates[(- 1)]):
        dateadj = self.cal.adjust(date, MODIFIEDFOLLOWING)
        if (date in self.dates):
            i += 1
            if (date != dateadj):
                print(('Error [%s] adjusted to %s, expected same' % (date, dateadj)))
                err_count += 1
        elif ((i >= 0) and (i < (len(self.dates) - 1))):
            j = (i + (0 if (dateadj.month != self.dates[(i + 1)].month) else 1))
            if (dateadj != self.dates[j]):
                print(('Error [%s] adjusted to %s, expected %s' % (date, dateadj, self.dates[j])))
                err_count += 1
        if (err_count > 10):
            break
        date += datetime.timedelta(days=1)
    assert (err_count == 0)
