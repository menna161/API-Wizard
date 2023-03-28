from croniter.croniter import croniter
from datetime import datetime
from tzlocal import get_localzone
from uuid import uuid4
import time
import functools
import asyncio
import sys
import inspect


def initialize(self):
    'Initialize croniter and related times'
    if (self.croniter is None):
        self.time = time.time()
        self.datetime = datetime.now(self.tz)
        self.loop_time = self.loop.time()
        self.croniter = croniter(self.spec, start_time=self.datetime, **self.croniter_kwargs)
