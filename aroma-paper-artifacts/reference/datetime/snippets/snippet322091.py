import os, sys, re, time, threading, _thread
import warnings, tempfile
import configparser, inspect, getpass, traceback
from datetime import datetime, timedelta, timezone
from collections.abc import Iterable
from html.parser import HTMLParser
import mastodon
from mastodon import Mastodon, StreamListener
from configobj import ConfigObj


def interval_threadproc(f):
    self.log(f.__name__, 'Started')
    t = datetime.now()
    tLast = t
    while True:
        self.alive.acquire()
        t = datetime.now()
        interval = interval_next(f, t, tLast)
        if (interval == 0):
            try:
                f()
            except Exception as e:
                error = 'Exception encountered in @interval function: {}\n{}'.format(repr(e), traceback.format_exc())
                self.report_error(error, f.__name__)
            t = datetime.now()
            interval = interval_next(f, t, t)
        if self.verbose:
            self.log((f.__name__ + '.debug'), 'Next wait interval: {}s'.format(interval))
        tLast = t
        self.alive.wait(max(interval, 1))
        if (self.state == PineappleBot.STOPPING):
            self.alive.release()
            self.log(f.__name__, 'Shutting down')
            return 0
        else:
            self.alive.release()
