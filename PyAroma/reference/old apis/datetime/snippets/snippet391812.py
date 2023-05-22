from __future__ import print_function, unicode_literals, division, absolute_import
import locale
import os, sys, unittest, tempfile, shutil, subprocess, re, json, platform
import time
import random
import functools
import datetime
from contextlib import contextmanager
import dxpy
from dxpy.compat import str, basestring, USING_PYTHON2


def decorator(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        daystr = datetime.datetime.today().strftime('%Y%m%d')
        with open('{0}.traceability.{1}.csv'.format(os.path.splitext(os.path.basename(__file__))[0], daystr), 'a') as f:
            secstr = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            try:
                retval = func(*args, **kwargs)
                for tid in id_array:
                    f.write('{0},{1},{2}\n'.format(tid, 'PASS', secstr))
                return retval
            except Exception as e:
                for tid in id_array:
                    f.write('{0},{1},{2}\n'.format(tid, 'FAIL', secstr))
                raise
    return wrapper
