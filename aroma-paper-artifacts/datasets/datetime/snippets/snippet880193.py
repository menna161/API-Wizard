import atexit
import datetime
from dateutil.parser import parse
import json
import mimetypes
from multiprocessing.pool import ThreadPool
import os
import re
import tempfile
from urllib.parse import quote
from polyaxon_sdk.configuration import Configuration
import polyaxon_sdk.models
from polyaxon_sdk import rest
from polyaxon_sdk.exceptions import ApiValueError, ApiException


def __deserialize_datetime(self, string):
    'Deserializes string to datetime.\n\n        The string should be in iso8601 datetime format.\n\n        :param string: str.\n        :return: datetime.\n        '
    try:
        return parse(string)
    except ImportError:
        return string
    except ValueError:
        raise rest.ApiException(status=0, reason='Failed to parse `{0}` as datetime object'.format(string))
