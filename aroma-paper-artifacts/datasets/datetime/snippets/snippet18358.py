import string
from weakref import ref as wkref
import copy
import sys
import warnings
import re
import sre_constants
import collections
import pprint
import traceback
import types
from datetime import datetime
from _thread import RLock
from collections import OrderedDict as _OrderedDict
import __builtin__
import uuid
from threading import RLock
from ordereddict import OrderedDict as _OrderedDict
import pdb


@staticmethod
def convertToDatetime(fmt='%Y-%m-%dT%H:%M:%S.%f'):
    '\n        Helper to create a parse action for converting parsed datetime string to Python datetime.datetime\n\n        Params -\n         - fmt - format to be passed to datetime.strptime (default=C{"%Y-%m-%dT%H:%M:%S.%f"})\n\n        Example::\n            dt_expr = pyparsing_common.iso8601_datetime.copy()\n            dt_expr.setParseAction(pyparsing_common.convertToDatetime())\n            print(dt_expr.parseString("1999-12-31T23:59:59.999"))\n        prints::\n            [datetime.datetime(1999, 12, 31, 23, 59, 59, 999000)]\n        '

    def cvt_fn(s, l, t):
        try:
            return datetime.strptime(t[0], fmt)
        except ValueError as ve:
            raise ParseException(s, l, str(ve))
    return cvt_fn
