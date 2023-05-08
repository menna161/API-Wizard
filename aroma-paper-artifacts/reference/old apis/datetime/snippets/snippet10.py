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


def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')
