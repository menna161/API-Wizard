import time
import datetime
import hashlib
import hmac
import json
from enum import Enum
import requests
from decimal import Decimal
from .version import __version__ as version


def get_time_stamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970, 1, 1)
    return str(int((d - epoch).total_seconds()))
