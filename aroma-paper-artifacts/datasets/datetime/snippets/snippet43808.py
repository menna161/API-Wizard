import re
from functools import wraps
import traceback
import logging


def json_date(date=None):
    'Given a db datetime, return a steemd/json-friendly version.'
    if (not date):
        return '1969-12-31T23:59:59'
    return 'T'.join(str(date).split(' '))
