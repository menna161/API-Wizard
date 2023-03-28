import datetime
import hashlib
import json
import random
import socket
import time
import os
import decimal
from copy import deepcopy
from dateutil.relativedelta import relativedelta
from requests.cookies import RequestsCookieJar
from atp.utils.common import read_custom


def convert_mysql_datatype_to_py(data):
    if isinstance(data, datetime.datetime):
        data = data.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(data, datetime.date):
        data = data.strftime('%Y-%m-%d')
    elif isinstance(data, decimal.Decimal):
        data = float(data)
    return data
