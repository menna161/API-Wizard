import re
import io
import datetime
from os import linesep
import sys
from os import path as op
from warnings import warn


def _dump_value(v):
    dump_funcs = {str: _dump_str, unicode: _dump_str, list: _dump_list, int: (lambda v: v), bool: (lambda v: unicode(v).lower()), float: _dump_float, datetime.datetime: (lambda v: v.isoformat().replace('+00:00', 'Z'))}
    dump_fn = dump_funcs.get(type(v))
    if ((dump_fn is None) and hasattr(v, '__iter__')):
        dump_fn = dump_funcs[list]
    return (dump_fn(v) if (dump_fn is not None) else dump_funcs[str](v))
