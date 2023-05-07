import contextlib
import datetime
import errno
import os
import pprint
import shutil
import signal
import socket
import sys
import tempfile
import time
import psutil
from psutil import AIX
from psutil import BSD
from psutil import FREEBSD
from psutil import LINUX
from psutil import MACOS
from psutil import NETBSD
from psutil import OPENBSD
from psutil import POSIX
from psutil import SUNOS
from psutil import WINDOWS
from psutil._compat import FileNotFoundError
from psutil._compat import long
from psutil.tests import ASCII_FS
from psutil.tests import check_net_address
from psutil.tests import CI_TESTING
from psutil.tests import DEVNULL
from psutil.tests import enum
from psutil.tests import get_test_subprocess
from psutil.tests import HAS_BATTERY
from psutil.tests import HAS_CPU_FREQ
from psutil.tests import HAS_GETLOADAVG
from psutil.tests import HAS_NET_IO_COUNTERS
from psutil.tests import HAS_SENSORS_BATTERY
from psutil.tests import HAS_SENSORS_FANS
from psutil.tests import HAS_SENSORS_TEMPERATURES
from psutil.tests import mock
from psutil.tests import PYPY
from psutil.tests import reap_children
from psutil.tests import retry_on_failure
from psutil.tests import safe_rmpath
from psutil.tests import TESTFN
from psutil.tests import TESTFN_UNICODE
from psutil.tests import TRAVIS
from psutil.tests import unittest
from psutil.tests.runner import run
import resource


@unittest.skipIf((CI_TESTING and (not psutil.users())), 'unreliable on CI')
def test_users(self):
    users = psutil.users()
    self.assertNotEqual(users, [])
    for user in users:
        assert user.name, user
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(user.terminal, (str, type(None)))
        if (user.host is not None):
            self.assertIsInstance(user.host, (str, type(None)))
        user.terminal
        user.host
        assert (user.started > 0.0), user
        datetime.datetime.fromtimestamp(user.started)
        if (WINDOWS or OPENBSD):
            self.assertIsNone(user.pid)
        else:
            psutil.Process(user.pid)
