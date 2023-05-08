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


def execution_history_all(self, symbol):
    now = datetime.datetime.now()
    from_ts = '2019-01-13T12:00:00.000Z'
    prev = now.strftime('%Y-%m-%dT12:00:00.000Z')
    print(prev)
    tx = self.execution_history(symbol, prev)
    return tx
