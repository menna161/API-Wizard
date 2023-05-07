import datetime
import sys
from contextlib import contextmanager
import shutil


def restart(self):
    self.start = datetime.datetime.now()
    self.end = None
