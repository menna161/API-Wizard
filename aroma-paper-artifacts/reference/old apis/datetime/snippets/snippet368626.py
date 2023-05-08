import abc
import time
from datetime import datetime, timedelta, date


def _get_date_values_since_initial_date(self, date_tuple):
    'Takes an intial date tuple and returns a computed set of date tuples until UTC now\n\n        Does _not_ include the original date tuple.\n        '
    partitions = []
    date_ints = list(map(int, date_tuple))
    initial_date = date(*date_ints)
    today = datetime.utcfromtimestamp(time.time()).date()
    for i in range((today - initial_date).days):
        new_date = (initial_date + timedelta(days=(i + 1)))
        part = new_date.isoformat().split('-')
        partitions.append(part)
    return partitions
