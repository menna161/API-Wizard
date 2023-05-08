from calendar import isleap, monthrange
from datetime import date, datetime, timedelta
from itertools import chain


def __init__(self, dates=None, today=None):
    '\n        :param dates: list of date ids (in string format)\n        :param today: datetime object\n        '
    self.dates = (sorted(dates, reverse=True) if dates else [])
    self.today = (today or date.today())
    self.white_list = tuple()
    self.black_list = tuple()
    self.run()
