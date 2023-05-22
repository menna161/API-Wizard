import calendar
import datetime
from email import utils as email_utils
import logging
import os
import re
from google.appengine.api import runtime
from google.appengine.api import runtime


def posix_to_dt_str(posix):
    'Reverse of str_to_datetime.\n\n  This is used by GCS stub to generate GET bucket XML response.\n\n  Args:\n    posix: A float of secs from unix epoch.\n\n  Returns:\n    A datetime str.\n  '
    dt = datetime.datetime.utcfromtimestamp(posix)
    dt_str = dt.strftime(_DT_FORMAT)
    return (dt_str + '.000Z')
