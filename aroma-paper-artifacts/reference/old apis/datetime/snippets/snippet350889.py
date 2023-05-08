from __future__ import print_function
import datetime as dt
import getpass
import locale
import logging
import sys
from dfvfs.lib import definitions
from dfvfs.lib import errors
from dfvfs.helpers import volume_scanner


def _format_timestamp(filetime):
    return str(dt.datetime.utcfromtimestamp(((filetime - _EPOCH_AS_FILETIME) / _HUNDREDS_OF_NANOSECONDS)).strftime(_TIME_FORMAT))
