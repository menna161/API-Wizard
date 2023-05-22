import calendar
import datetime
from email import utils as email_utils
import logging
import os
import re
from google.appengine.api import runtime
from google.appengine.api import runtime


def dt_str_to_posix(dt_str):
    "format str to posix.\n\n  datetime str is of format %Y-%m-%dT%H:%M:%S.%fZ,\n  e.g. 2013-04-12T00:22:27.978Z. According to ISO 8601, T is a separator\n  between date and time when they are on the same line.\n  Z indicates UTC (zero meridian).\n\n  A pointer: http://www.cl.cam.ac.uk/~mgk25/iso-time.html\n\n  This is used to parse LastModified node from GCS's GET bucket XML response.\n\n  Args:\n    dt_str: A datetime str.\n\n  Returns:\n    A float of secs from unix epoch. By posix definition, epoch is midnight\n    1970/1/1 UTC.\n  "
    (parsable, _) = dt_str.split('.')
    dt = datetime.datetime.strptime(parsable, _DT_FORMAT)
    return calendar.timegm(dt.utctimetuple())
