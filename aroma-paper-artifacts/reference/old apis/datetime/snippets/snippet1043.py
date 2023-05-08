import requests
import json
import re
import pytz
import datetime
import time
from dao.redis_dao import predict_insert_
from sklearn.linear_model import LinearRegression


def change_int(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    return dt
