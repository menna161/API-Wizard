import datetime
import gzip
import json
import logging
import random
import re
import redis
import requests
import StringIO
import time
from requests.exceptions import RequestException
from timeit import default_timer as timer


def prepare_result_recursively(result, kind, timestamp=None):
    ret = []
    if isinstance(result, dict):
        result = result.copy()
        timestamp = (result.pop('_stamp', timestamp) or datetime.datetime.utcnow().isoformat())
        kind = '.'.join(filter(None, [kind, result.pop('_type', None)]))
        lone_key = (next(iter(result)) if (len(result) == 1) else None)
        if ((lone_key != None) and isinstance(result[lone_key], list)):
            ret.extend(prepare_result_recursively(result[lone_key], kind, timestamp))
        elif result:
            result.update({'@ts': timestamp, '@t': kind})
            ret.append(result)
    elif isinstance(result, (list, set, tuple)):
        timestamp = (timestamp or datetime.datetime.utcnow().isoformat())
        for res in result:
            ret.extend(prepare_result_recursively(res, kind, timestamp))
    else:
        ret.append({'@ts': (timestamp or datetime.datetime.utcnow().isoformat()), '@t': kind, 'value': result})
    return ret
