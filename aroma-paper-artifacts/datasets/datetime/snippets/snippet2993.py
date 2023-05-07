import json
import hashlib
from datetime import datetime
from urllib.parse import urlparse
import logging


def retrieve_datetime(datetime_isoformat):
    try:
        return datetime.strptime(datetime_isoformat, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.strptime(datetime_isoformat, '%Y-%m-%dT%H:%M:%S')
