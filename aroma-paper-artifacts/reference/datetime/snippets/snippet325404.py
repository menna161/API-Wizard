import sys
import urllib.request
import datetime
import requests
import re
import time
import types
import http.client
from pyquery import PyQuery as pq


@staticmethod
def datetimeToUnixtime(_datetime):
    return time.mktime(_datetime.timetuple())
