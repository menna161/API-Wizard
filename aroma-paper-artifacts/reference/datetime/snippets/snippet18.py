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


def validate_date_str(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
