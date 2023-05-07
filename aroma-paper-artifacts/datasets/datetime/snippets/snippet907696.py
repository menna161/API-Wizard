import datetime
import warnings
from business_calendar import Calendar, FOLLOWING, PREVIOUS, MODIFIEDFOLLOWING
from dateutil.rrule import rruleset, rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
from dateutil.parser import parse


def test_adjust_following(self):
    print('test_adjust_following')
    err_count = 0
    i = (- 1)
    date = self.dates[0]
    while (date <= self.dates[(- 1)]):
        dateadj = self.cal.adjust(date, FOLLOWING)
        if (date in self.dates):
            i += 1
            if (date != dateadj):
                print(('Error [%s] adjusted to %s, expected same' % (date, dateadj)))
                err_count += 1
        elif (i < (len(self.dates) - 1)):
            if (dateadj != self.dates[(i + 1)]):
                print(('Error [%s] adjusted to %s, expected %s' % (date, dateadj, self.dates[(i + 1)])))
                err_count += 1
        if (err_count > 10):
            break
        date += datetime.timedelta(days=1)
    assert (err_count == 0)
