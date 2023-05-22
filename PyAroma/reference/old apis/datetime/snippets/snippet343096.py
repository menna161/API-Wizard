import requests
from time import sleep
import json
from . import errors
import math
import uuid
from .accessTokenAuth import AccessTokenAuth
from .apiKeyAuthWithExpires import APIKeyAuthWithExpires
from archon.util.custom_logger import setup_logger
import datetime
from datetime import timedelta
import logging
import time


def history(self, start):
    n = datetime.datetime.now()
    start_day = datetime.datetime(start.year, start.month, start.day)
    cur = start_day
    all_candles = list()
    while (cur < n):
        cur += timedelta(hours=24)
        self.logger.debug(('fetch %s' % str(cur)))
        d = self.get_minute_1day(cur)
        all_candles += d
    return all_candles
