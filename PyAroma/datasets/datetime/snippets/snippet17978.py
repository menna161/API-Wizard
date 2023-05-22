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
def convertToDate(fmt='%Y-%m-%d'):
    '\n        Helper to create a parse action for converting parsed date string to Python datetime.date\n\n        Params -\n         - fmt - format to be passed to datetime.strptime (default=C{"%Y-%m-%d"})\n\n        Example::\n            date_expr = pyparsing_common.iso8601_date.copy()\n            date_expr.setParseAction(pyparsing_common.convertToDate())\n            print(date_expr.parseString("1999-12-31"))\n        prints::\n            [datetime.date(1999, 12, 31)]\n        '

    def cvt_fn(s, l, t):
        try:
            return datetime.strptime(t[0], fmt).date()
        except ValueError as ve:
            raise ParseException(s, l, str(ve))
    return cvt_fn
