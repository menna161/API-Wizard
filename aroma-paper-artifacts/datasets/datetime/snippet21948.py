import datetime
import re
import sys
from pip._vendor.toml.decoder import InlineTableDict


def __init__(self, _dict=dict, preserve=False):
    self._dict = _dict
    self.preserve = preserve
    self.dump_funcs = {str: _dump_str, unicode: _dump_str, list: self.dump_list, bool: (lambda v: unicode(v).lower()), int: (lambda v: v), float: _dump_float, datetime.datetime: (lambda v: v.isoformat().replace('+00:00', 'Z')), datetime.time: _dump_time, datetime.date: (lambda v: v.isoformat())}
