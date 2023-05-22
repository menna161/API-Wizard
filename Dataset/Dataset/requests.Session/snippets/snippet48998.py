import logging
import threading
import sys
import requests
from contextlib import contextmanager
from time import time


def session(self):
    return requests.Session()
