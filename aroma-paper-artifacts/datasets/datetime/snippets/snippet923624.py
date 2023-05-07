import datetime
import errno
import os
import re
import subprocess
import time
import psutil
from psutil import AIX
from psutil import BSD
from psutil import LINUX
from psutil import MACOS
from psutil import OPENBSD
from psutil import POSIX
from psutil import SUNOS
from psutil.tests import CI_TESTING
from psutil.tests import get_kernel_version
from psutil.tests import get_test_subprocess
from psutil.tests import HAS_NET_IO_COUNTERS
from psutil.tests import mock
from psutil.tests import PYTHON_EXE
from psutil.tests import reap_children
from psutil.tests import retry_on_failure
from psutil.tests import sh
from psutil.tests import skip_on_access_denied
from psutil.tests import TRAVIS
from psutil.tests import unittest
from psutil.tests import wait_for_pid
from psutil.tests import which
from psutil.tests.runner import run


@unittest.skipIf((MACOS or BSD), 'ps -o start not available')
def test_create_time(self):
    time_ps = ps('start', self.pid)
    time_psutil = psutil.Process(self.pid).create_time()
    time_psutil_tstamp = datetime.datetime.fromtimestamp(time_psutil).strftime('%H:%M:%S')
    round_time_psutil = round(time_psutil)
    round_time_psutil_tstamp = datetime.datetime.fromtimestamp(round_time_psutil).strftime('%H:%M:%S')
    self.assertIn(time_ps, [time_psutil_tstamp, round_time_psutil_tstamp])
