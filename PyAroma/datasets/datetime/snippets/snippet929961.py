from typing import List, Dict, Tuple
from urllib.parse import urlencode, quote
from base64 import b64encode
import math
import datetime
import json
from Crypto.Cipher import AES
from qdata.errors import ErrorCode, QdataError
import requests


def get_time_range_list(startdate: str, enddate: str) -> List[Tuple[(str, str)]]:
    '\n        切分时间段\n    '
    date_range_list = []
    startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    while 1:
        tempdate = (startdate + datetime.timedelta(days=300))
        if (tempdate > enddate):
            date_range_list.append((startdate, enddate))
            break
        date_range_list.append((startdate, tempdate))
        startdate = (tempdate + datetime.timedelta(days=1))
    return date_range_list
