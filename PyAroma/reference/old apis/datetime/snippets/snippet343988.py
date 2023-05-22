import hmac
import base64
import time
import datetime
from . import consts as c


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat('T', 'milliseconds')
    return (t + 'Z')
