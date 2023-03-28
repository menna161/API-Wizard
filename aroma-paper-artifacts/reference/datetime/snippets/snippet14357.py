import wx.grid
import os, time, datetime, shutil
from ast import literal_eval
from shlex import shlex
import logger


def prettyDate(val, long=True):
    if isinstance(val, datetime.datetime):
        val = val.timetuple()
    if (not isinstance(val, time.struct_time)):
        val = time.localtime(val)
    if long:
        return time.strftime('%Y-%m-%d %H:%M:%S', val)
    else:
        return time.strftime('%Y-%m-%d', val)
