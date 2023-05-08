import dateparser
from datetime import datetime
import pytz


def date_to_seconds(date_str):
    'Convert UTC date to seconds\n    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"\n    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/\n    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"\n    :type date_str: str\n    '
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    d = dateparser.parse(date_str)
    if ((d.tzinfo is None) or (d.tzinfo.utcoffset(d) is None)):
        d = d.replace(tzinfo=pytz.utc)
    return int((d - epoch).total_seconds())
