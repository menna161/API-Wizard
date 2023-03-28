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


def history_days(self, numdays):
    n = datetime.datetime.now()
    start = (n - datetime.timedelta(days=numdays))
    candles = self.history(start)
    return candles
