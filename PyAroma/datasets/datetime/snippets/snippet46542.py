from __future__ import absolute_import, division, print_function, unicode_literals
import datetime
import json
import logging
import pkg_resources
import re
import six
import socket
import sys
import time
import uuid
from functools import wraps
import requests
from .auth import AuthHandler
from requests.exceptions import Timeout, ConnectionError
from .exceptions import GenieHTTPError


def dttm_to_epoch(date_str, frmt='%Y-%m-%dT%H:%M:%SZ'):
    'Convert a date string to epoch seconds.'
    return int((datetime.datetime.strptime(date_str, frmt) - datetime.datetime(1970, 1, 1)).total_seconds())
