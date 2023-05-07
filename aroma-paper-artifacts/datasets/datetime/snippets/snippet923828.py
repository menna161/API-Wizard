import datetime
import errno
import glob
import os
import platform
import re
import signal
import subprocess
import sys
import time
import warnings
import psutil
from psutil import WINDOWS
from psutil._compat import FileNotFoundError
from psutil.tests import APPVEYOR
from psutil.tests import get_test_subprocess
from psutil.tests import HAS_BATTERY
from psutil.tests import mock
from psutil.tests import PY3
from psutil.tests import PYPY
from psutil.tests import reap_children
from psutil.tests import retry_on_failure
from psutil.tests import sh
from psutil.tests import unittest
from psutil.tests.runner import run
import win32api
import win32con
import win32process
import wmi
import ctypes
import ctypes.wintypes
from psutil._pswindows import convert_oserror
from psutil._pswindows import ACCESS_DENIED_SET


def test_boot_time(self):
    wmi_os = wmi.WMI().Win32_OperatingSystem()
    wmi_btime_str = wmi_os[0].LastBootUpTime.split('.')[0]
    wmi_btime_dt = datetime.datetime.strptime(wmi_btime_str, '%Y%m%d%H%M%S')
    psutil_dt = datetime.datetime.fromtimestamp(psutil.boot_time())
    diff = abs((wmi_btime_dt - psutil_dt).total_seconds())
    self.assertLessEqual(diff, 3)
