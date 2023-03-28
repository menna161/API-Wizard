from __future__ import print_function, unicode_literals, division, absolute_import
import datetime, time, json, math, sys, copy
import locale
import subprocess
from collections import defaultdict
import dxpy
from .printing import RED, GREEN, BLUE, YELLOW, WHITE, BOLD, UNDERLINE, ENDC, DELIMITER, get_delimiter, fill
from .pretty_print import format_timedelta
from ..compat import basestring, USING_PYTHON2
from ..bindings.search import find_one_data_object
from ..exceptions import DXError
from dxpy.api import job_describe


def render_timestamp(timestamp):
    return datetime.datetime.fromtimestamp((timestamp // 1000)).ctime()
