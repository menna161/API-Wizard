import base64
import datetime
import hashlib
import locale
import os
import re
import telnetlib
import time
import urllib
import platform
from urllib.parse import quote


def datetime_str_timestamp(datetime_str):
    d = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(d.timetuple()))
