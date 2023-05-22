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
from itertools import filterfalse
from _thread import RLock
from collections.abc import Iterable
from collections.abc import MutableMapping
from collections import OrderedDict as _OrderedDict
from types import SimpleNamespace
import __builtin__
import uuid
from itertools import ifilterfalse as filterfalse
from threading import RLock
from collections import Iterable
from collections import MutableMapping
import inspect
from ordereddict import OrderedDict as _OrderedDict
import pdb


def cvt_fn(s, l, t):
    try:
        return datetime.strptime(t[0], fmt)
    except ValueError as ve:
        raise ParseException(s, l, str(ve))
