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
def getStrTime(time=datetime.datetime.now(), format='%Y-%m-%d'):
    try:
        return time.__format__(format)
    except:
        return None
