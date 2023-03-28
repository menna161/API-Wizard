import datetime
import sys
import io
import time
import unittest
from xml.sax import saxutils


def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
    self.stream = stream
    self.verbosity = verbosity
    if (title is None):
        self.title = self.DEFAULT_TITLE
    else:
        self.title = title
    if (description is None):
        self.description = self.DEFAULT_DESCRIPTION
    else:
        self.description = description
    self.startTime = datetime.datetime.now()
