import re
import logging
import ujson as json


def valid_date(val):
    'Valid datetime (YYYY-MM-DDTHH:MM:SS)'
    assert VALID_DATE.match(val), ('invalid date: %s' % val)
    return val
