from __future__ import absolute_import, division, print_function, with_statement
from collections import defaultdict
from datetime import datetime
import functools
import time
import sys
from bson.objectid import ObjectId
from turbo.log import model_log
from turbo.util import escape as _es, import_object


@staticmethod
def utcdatetime(dt=None):
    if dt:
        return datetime.strptime(dt, '%Y-%m-%d %H:%M')
    else:
        return datetime.utcnow()
