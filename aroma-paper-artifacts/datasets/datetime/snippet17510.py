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
from operator import itemgetter
import itertools
from functools import wraps
from contextlib import contextmanager
from itertools import filterfalse
from _thread import RLock
from collections.abc import Iterable
from collections.abc import MutableMapping, Mapping
from collections import OrderedDict as _OrderedDict
from types import SimpleNamespace
import __builtin__
import uuid
from itertools import ifilterfalse as filterfalse
from threading import RLock
from collections import Iterable
from collections import MutableMapping, Mapping
import inspect
from ordereddict import OrderedDict as _OrderedDict
import pdb


@staticmethod
def convertToDatetime(fmt='%Y-%m-%dT%H:%M:%S.%f'):
    'Helper to create a parse action for converting parsed\n        datetime string to Python datetime.datetime\n\n        Params -\n         - fmt - format to be passed to datetime.strptime (default= ``"%Y-%m-%dT%H:%M:%S.%f"``)\n\n        Example::\n\n            dt_expr = pyparsing_common.iso8601_datetime.copy()\n            dt_expr.setParseAction(pyparsing_common.convertToDatetime())\n            print(dt_expr.parseString("1999-12-31T23:59:59.999"))\n\n        prints::\n\n            [datetime.datetime(1999, 12, 31, 23, 59, 59, 999000)]\n        '

    def cvt_fn(s, l, t):
        try:
            return datetime.strptime(t[0], fmt)
        except ValueError as ve:
            raise ParseException(s, l, str(ve))
    return cvt_fn
