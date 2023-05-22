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


def get_repayment_plan_dic(start_timestamp, term_total, capital_no=None):
    '\n    根据传入时间获取每月罚息时间\n    '
    if isinstance(start_timestamp, int):
        start_timestamp = int(str(start_timestamp)[:10])
    elif isinstance(start_timestamp, str):
        start_timestamp = int(start_timestamp[:10])
    else:
        return {}
    term_total = int(term_total)
    big_month = [1, 3, 5, 7, 8, 10, 12]
    term_no = 0
    start_time = datetime.datetime.fromtimestamp(start_timestamp)
    plan_dic = {}
    plus_month = (start_time + relativedelta(months=(+ 1)))
    term_start_time = start_time
    while (term_no < term_total):
        term_no += 1
        plan_dic[term_no] = [term_start_time, plus_month]
        term_start_time = plus_month
        plus_month += relativedelta(months=(+ 1))
        if ((plus_month.day < start_time.day) and (plus_month.month in big_month)):
            plus_month += relativedelta(days=(+ (start_time.day - plus_month.day)))
    format_plan_dic = {}
    for (term_no, time_list) in plan_dic.items():
        if (term_no == term_total):
            if (capital_no == '045'):
                time_list[1] = (time_list[1] + relativedelta(days=(- 1)))
        format_plan_dic[term_no] = [str(time_list[0])[0:10], str(time_list[1])[0:10]]
    return format_plan_dic
