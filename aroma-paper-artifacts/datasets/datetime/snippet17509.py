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
def convertToDate(fmt='%Y-%m-%d'):
    '\n        Helper to create a parse action for converting parsed date string to Python datetime.date\n\n        Params -\n         - fmt - format to be passed to datetime.strptime (default= ``"%Y-%m-%d"``)\n\n        Example::\n\n            date_expr = pyparsing_common.iso8601_date.copy()\n            date_expr.setParseAction(pyparsing_common.convertToDate())\n            print(date_expr.parseString("1999-12-31"))\n\n        prints::\n\n            [datetime.date(1999, 12, 31)]\n        '

    def cvt_fn(s, l, t):
        try:
            return datetime.strptime(t[0], fmt).date()
        except ValueError as ve:
            raise ParseException(s, l, str(ve))
    return cvt_fn
