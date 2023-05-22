import datetime
import hashlib
import json
import random
import socket
import time
import os
import decimal
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from requests.cookies import RequestsCookieJar
from atp.utils.common import read_custom


def default(self, obj):
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    elif isinstance(obj, bytes):
        return str(obj, encoding='utf-8')
    elif isinstance(obj, type):
        return str(obj)
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, RequestsCookieJar):
        return dict(obj)
    return json.JSONEncoder.default(self, obj)
