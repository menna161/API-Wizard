import datetime
from logger import Logger


def _get_date(self):
    return str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
