import os
import sys
import io
import logging
import time
import datetime
import traceback
import six
import pyocd
from ..core import exceptions


def handle_sys_time(self, args):
    now = datetime.datetime.now()
    delta = (now - self.EPOCH)
    seconds = ((delta.days * 86400) + delta.seconds)
    return seconds
