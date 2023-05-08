import os
import time
import logging
import argparse
from weakref import proxy
from threading import Thread
from datetime import datetime
from collections import deque
from . import LOGO
from .__version__ import __version__
from .parser import HTTPLogParser
from .display import Display
from .metrics import AlertMetric, TaggedCounterMetric, CounterMetric


def add_point(self, http_data):
    self.hit_total += 1
    self.last_seen = datetime.now()
    self.alert_metric.add_point()
    self.traffic_counter.add_point()
    self.subpath_counter.add_point(tags=[http_data['subpath']])
