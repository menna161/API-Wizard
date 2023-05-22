import logging
import threading
import sys
import requests
from contextlib import contextmanager
from time import time


def requests_proxy(self, method, url, **kwargs):
    '\n        request proxy\n        '
    proxies = {'http': 'socks5://127.0.0.1:1086', 'https': 'socks5://127.0.0.1:1086'}
    response = requests.request(method, url, **kwargs)
    return response
