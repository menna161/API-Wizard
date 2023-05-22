import logging
import math
import decimal
from datetime import datetime
from pytz import utc
import ujson as json


def parse_time(block_time):
    'Convert chain date into datetime object.'
    return datetime.strptime(block_time, '%Y-%m-%dT%H:%M:%S')
