import time
import datetime
import hashlib
import hmac
import json
from enum import Enum
import requests
from decimal import Decimal
from .version import __version__ as version


def get_price_history(self, symbol, duration=5, resolution=1):
    if ((duration / resolution) >= 500):
        raise Exception('Too many Data points')
    current_timestamp = time.mktime(datetime.datetime.today().timetuple())
    last_timestamp = (current_timestamp - (duration * 60))
    query = {'symbol': symbol, 'from': last_timestamp, 'to': current_timestamp, 'resolution': resolution}
    response = self._request('GET', 'chart/history', query=query)
    return response.json()
