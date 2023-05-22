from __future__ import absolute_import, print_function
import argparse
import json
import multiprocessing.pool
import os
import re
import requests
import signal
import sys
import subprocess
import time
from io import BytesIO
from threading import Thread, Lock, Event
from jupyter_core.paths import jupyter_runtime_dir
from ipython_genutils.py3compat import bytes_to_str, which
from notebook._sysinfo import get_sys_info
from ipython_genutils.tempdir import TemporaryDirectory
from unittest.mock import patch
from subprocess import TimeoutExpired
import notebook.tests as t
import glob
from mock import patch
import traceback


def setup(self):
    self.ipydir = TemporaryDirectory()
    self.config_dir = TemporaryDirectory()
    self.nbdir = TemporaryDirectory()
    self.home = TemporaryDirectory()
    self.env = {'HOME': self.home.name, 'JUPYTER_CONFIG_DIR': self.config_dir.name, 'IPYTHONDIR': self.ipydir.name}
    self.dirs.append(self.ipydir)
    self.dirs.append(self.home)
    self.dirs.append(self.config_dir)
    self.dirs.append(self.nbdir)
    os.makedirs(os.path.join(self.nbdir.name, os.path.join(u'sub ∂ir1', u'sub ∂ir 1a')))
    os.makedirs(os.path.join(self.nbdir.name, os.path.join(u'sub ∂ir2', u'sub ∂ir 1b')))
    if self.xunit:
        self.add_xunit()
    if self.url:
        try:
            alive = (requests.get(self.url).status_code == 200)
        except:
            alive = False
        if alive:
            self.cmd.append(('--url=%s' % self.url))
        else:
            raise Exception(('Could not reach "%s".' % self.url))
    else:
        self.server_port = 0
        self._init_server()
        if self.server_port:
            self.cmd.append(('--url=http://localhost:%i%s' % (self.server_port, self.base_url)))
        else:
            self.cmd = [sys.executable, '-c', 'raise SystemExit(1)']
