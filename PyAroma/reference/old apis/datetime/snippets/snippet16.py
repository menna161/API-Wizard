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


def get_gmt_time(text):
    '\n    Fri Oct 025 2019 00:00:00 GMT+0800 (中国标准时间)\n    Sun Oct 06 2019 00:00:00 GMT+0800 (中国标准时间)\n    :param text:\n    :return:\n    '
    return datetime.datetime.strptime(text, '%Y-%m-%d').strftime(GMT_FORMAT)
