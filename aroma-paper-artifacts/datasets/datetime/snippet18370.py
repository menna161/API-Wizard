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


def cvt_fn(s, l, t):
    try:
        return datetime.strptime(t[0], fmt).date()
    except ValueError as ve:
        raise ParseException(s, l, str(ve))
