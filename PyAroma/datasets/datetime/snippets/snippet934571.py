import datetime
import sys
from contextlib import contextmanager
import shutil


def stop(self):
    self.end = datetime.datetime.now()
