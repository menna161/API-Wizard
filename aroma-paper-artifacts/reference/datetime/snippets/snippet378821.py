import datetime
import logging
import re
import signal
import threading
from timeit import default_timer as timer
import cProfile as profile


def set(self):
    self.timestamp = datetime.datetime.utcnow()
    super(TimedEvent, self).set()
