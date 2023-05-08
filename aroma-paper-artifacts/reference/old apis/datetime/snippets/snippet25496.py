from calendar import isleap, monthrange
from datetime import date, datetime, timedelta
from itertools import chain


def run(self):
    '\n        Feeds `self.white_list` and `self.black_list` with the dates do be kept\n        and deleted (respectively)\n        '
    last_w = (self.today - timedelta(days=7))
    last_m = (self.today - timedelta(days=self.get_last_month_length()))
    last_y = (self.today - timedelta(days=self.get_last_year_length()))
    backups_week = list()
    backups_month = list()
    backups_year = list()
    backups_older = list()
    for timestamp in self.dates:
        datetime_ = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        date_ = date(datetime_.year, datetime_.month, datetime_.day)
        if (date_ >= last_w):
            backups_week.append(timestamp)
        elif (date_ >= last_m):
            backups_month.append(timestamp)
        elif (date_ >= last_y):
            backups_year.append(timestamp)
        else:
            backups_older.append(timestamp)
    self.white_list = tuple(chain(backups_week, self.filter_dates(backups_month, 'week'), self.filter_dates(backups_year, 'month'), self.filter_dates(backups_older, 'year')))
    diff_as_tuple = tuple((set(self.dates) - set(self.white_list)))
    self.black_list = tuple(sorted(diff_as_tuple, reverse=True))
