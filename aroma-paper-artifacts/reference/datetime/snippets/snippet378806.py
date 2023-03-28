import datetime
import logging
import re
import signal
import threading
from timeit import default_timer as timer
import cProfile as profile


def run(self):
    if PROFILING:
        prof_file = '/tmp/{:%Y%m%d%H%M%S}_{:}.prof'.format(datetime.datetime.now(), self.name)
        log.warning("Profiling worker thread '%s' - after thread termination stats file will be written to: %s", self.name, prof_file)
        profile.runctx('self.work()', globals(), locals(), prof_file)
        log.info('Profiling stats written to: %s', prof_file)
    else:
        self.work()
