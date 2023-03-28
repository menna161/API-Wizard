import os, sys, re, time, threading, _thread
import warnings, tempfile
import configparser, inspect, getpass, traceback
from datetime import datetime, timedelta, timezone
from collections.abc import Iterable
from html.parser import HTMLParser
import mastodon
from mastodon import Mastodon, StreamListener
from configobj import ConfigObj


def startup(self):
    self.state = PineappleBot.STARTING
    self.log(None, 'Starting {0} {1}'.format(self.__class__.__name__, self.name))
    try:
        self.start()
    except Exception as e:
        self.log(None, 'Fatal exception: {}\n{}'.format(repr(e), traceback.format_exc()))
        return

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
    for (fname, f) in inspect.getmembers(self, predicate=inspect.ismethod):
        if (hasattr(f, 'interval') or hasattr(f, 'schedule')):
            t = threading.Thread(args=(f,), target=interval_threadproc)
            t.start()
            self.threads.append(t)
        if hasattr(f, 'reply'):
            self.reply_funcs.append(f)
        if hasattr(f, 'error_reporter'):
            self.report_funcs.append(f)
    if (len(self.reply_funcs) > 0):
        self.stream = self.mastodon.stream_user(self, run_async=True, reconnect_async=True)
    credentials = self.mastodon.account_verify_credentials()
    self.account_info = credentials
    self.username = credentials['username']
    self.default_visibility = credentials['source']['privacy']
    self.default_sensitive = credentials['source']['sensitive']
    self.state = PineappleBot.RUNNING
    self.log(None, 'Startup complete.')
