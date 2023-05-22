import requests
import json
import re
import pytz
import datetime
import time


def change_time(timestamp):
    timestamp = (timestamp / 1000)
    time_local = time.localtime(timestamp)
    dt = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    return dt
