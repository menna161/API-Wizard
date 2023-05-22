import datetime
import os
import re
import time
import psutil
from psutil import BSD
from psutil import FREEBSD
from psutil import NETBSD
from psutil import OPENBSD
from psutil.tests import get_test_subprocess
from psutil.tests import HAS_BATTERY
from psutil.tests import MEMORY_TOLERANCE
from psutil.tests import reap_children
from psutil.tests import retry_on_failure
from psutil.tests import sh
from psutil.tests import unittest
from psutil.tests import which
from psutil.tests.runner import run


def test_boot_time(self):
    s = sysctl('kern.boottime')
    sys_bt = datetime.datetime.strptime(s, '%a %b %d %H:%M:%S %Y')
    psutil_bt = datetime.datetime.fromtimestamp(psutil.boot_time())
    self.assertEqual(sys_bt, psutil_bt)
