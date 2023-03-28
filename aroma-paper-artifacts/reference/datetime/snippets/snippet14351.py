import wx.grid
import os, time, datetime, shutil
from ast import literal_eval
from shlex import shlex
import logger


def strToIsoDate(val):
    zpos = val.find('Z')
    if (zpos > 0):
        l = zpos
    else:
        l = len(val)
    if (l < 8):
        return val
    elif (l < 10):
        fmtstr = '%Y%m%d'
    elif (l < 14):
        fmtstr = '%Y%m%d%H%M'
    else:
        l = 14
        fmtstr = '%Y%m%d%H%M%S'
    try:
        ts = time.strptime(val[:l], fmtstr)
    except Exception as e:
        logger.error('Invalid datetime format %s: %s', val, e)
        return val
    try:
        gmt = time.mktime(ts)
    except Exception as e:
        logger.error('Invalid datetime format %s: %s', val, e)
        return val
    if (zpos > 0):
        ts = time.localtime(gmt)
        if (ts.tm_isdst > 0):
            gmt -= time.altzone
        else:
            gmt -= time.timezone
        zpi = val[(zpos + 1):]
        if zpi:
            try:
                gmt += (3600 * zpi)
            except:
                logger.error('Invalid time zone %s', val)
                pass
    return prettyDate(gmt, True)
