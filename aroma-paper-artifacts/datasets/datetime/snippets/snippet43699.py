import logging
import math
import decimal
from datetime import datetime
from pytz import utc
import ujson as json


def block_date(block):
    'Parse block timestamp into datetime object.'
    return parse_time(block['timestamp'])
