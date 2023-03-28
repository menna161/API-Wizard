import datetime
import re
from enum import Enum
from flask_babel import _
from .model import AppKernelException


def _is_date(self, validable_object):
    return isinstance(validable_object, (datetime.datetime, datetime.date))
