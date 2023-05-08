from calendar import isleap, monthrange
from datetime import date, datetime, timedelta
from itertools import chain


def filter_dates(self, dates, period):
    '\n        :param dates: list of ordered date ids (in string format)\n        :param period: a string for comparison (week, month or year)\n        :return: list of dates containing the most recent dates of each period\n        '
    reference = datetime.strftime(self.today, '%Y%m%d%H%M%S')
    method_mapping = {'week': (lambda obj: getattr(obj, 'isocalendar')()[1]), 'month': (lambda obj: getattr(obj, 'month')), 'year': (lambda obj: getattr(obj, 'year'))}
    for as_string in dates:
        as_date = datetime.strptime(as_string, '%Y%m%d%H%M%S')
        comparison = method_mapping.get(period)(as_date)
        reference_as_date = datetime.strptime(reference, '%Y%m%d%H%M%S')
        if (comparison != method_mapping.get(period)(reference_as_date)):
            reference = as_string
            (yield as_string)
