import os, sys, re, time, threading, _thread
import warnings, tempfile
import configparser, inspect, getpass, traceback
from datetime import datetime, timedelta, timezone
from collections.abc import Iterable
from html.parser import HTMLParser
import mastodon
from mastodon import Mastodon, StreamListener
from configobj import ConfigObj


def log(self, id, msg):
    if (id == None):
        id = self.name
    else:
        id = ((self.name + '.') + id)
    ts = datetime.now()
    msg_f = '[{0:%Y-%m-%d %H:%M:%S}] {1}: {2}'.format(ts, id, msg)
    if (self.log_file.closed or self.log_to_stderr):
        print(msg_f, file=sys.stderr)
    elif (not self.log_file.closed):
        print(msg_f, file=self.log_file, flush=True)
