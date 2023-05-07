import logging
import math
import decimal
from datetime import datetime
from pytz import utc
import ujson as json


def utc_timestamp(date):
    'Convert datetime to UTC unix timestamp.'
    return date.replace(tzinfo=utc).timestamp()
