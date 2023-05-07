import re
import io
import datetime
from os import linesep
import sys
from os import path as op
from warnings import warn


def utcoffset(self, dt):
    return (self._sign * datetime.timedelta(hours=self._hours, minutes=self._minutes))
