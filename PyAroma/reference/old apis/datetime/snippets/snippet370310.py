import datetime
import json
import os
import random
import re
import string
import time
from atp.httprunner.compat import basestring, builtin_str, integer_types, str
from atp.httprunner.exceptions import ParamsError
from requests_toolbelt import MultipartEncoder


def get_current_date(fmt='%Y-%m-%d'):
    ' get current date, default format is %Y-%m-%d\n    '
    return datetime.datetime.now().strftime(fmt)
