from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import datetime
import functools
import linecache
import os
import re
import time
import xml.dom.minidom
import opencue


def ETADateTime(job, frame):
    'Calculates ETA and returns it as a datetime.'
    eta = FrameEtaGenerator()
    time_left = eta.GetFrameEta(job, frame)['time_left']
    t = datetime.datetime.now()
    now_epoch = time.mktime(t.timetuple())
    time_left = datetime.datetime.fromtimestamp((time_left + now_epoch))
    return time_left
