import calendar
import datetime
import json
import time
import random
import traceback
import inspect
import importlib
from dateutil.relativedelta import relativedelta
from atp.api.disconf_executor import disconf_execute, disconf_execute_new
from atp.api.http_client import HttpClient
from atp.api.mysql_sql_executor import sql_execute, db_operation_to_json, sql_execute_with_params
from atp.api.ssh_executor import server_upload_file
from atp.utils.encryption import Encryption
from atp.utils.tools import is_json_contains, generate_idcard, generate_random_num, json_loads, generate_phone, generate_bank_card_no, generate_random_str, get_sign_common, transfer_json_string_to_dict, get_repayment_plan_dic, generate_compute_expression, convert_mysql_datatype_to_py
from atp.views.wrappers import custom_func_wrapper
from atp.api.ssh_client import SSHClient
from atp.api.get_log_content import GetLogContent
from atp.api.redis_api import RedisUtils
from atp.httprunner import logger as hr_logger
from atp.api.comm_log import logger
import os
from atp.app import create_app
import os


@custom_func_wrapper
def get_deltatimestamp(length, change=None):
    ' 时间-获取增量时间戳 : 位数, 增量\n    :desc: 说明: 获取当前的时间戳，加上增量，返回10位或13位数字\n    :param length:位数: 时间戳的位数，10或者13 二选一\n    :param change:增量: 增减时间的量，+代表增加，-代表减去，d代表天，h代表小时，m代表分钟，s代表秒，例如 +3d 或 -10m 或 +50s\n    '
    now_time = datetime.datetime.now()
    if change:
        change = change.upper()
        unit_li = ['D', 'H', 'M', 'S']
        unit_dic = {'D': None, 'H': None, 'M': None, 'S': None}
        for k in unit_li:
            change_list = change.split(k)
            if (len(change_list) == 2):
                unit_dic[k] = change_list[0]
                change = change_list[1]
            elif (len(change_list) == 1):
                change = change_list[0]
            else:
                return 'Error'
        for (k, v) in unit_dic.items():
            if v:
                if (k == 'D'):
                    now_time += datetime.timedelta(days=int(v))
                elif (k == 'H'):
                    now_time += datetime.timedelta(hours=int(v))
                elif (k == 'M'):
                    now_time += datetime.timedelta(minutes=int(v))
                elif (k == 'S'):
                    now_time += datetime.timedelta(seconds=int(v))
    if (str(length) == '10'):
        return int(time.mktime(now_time.timetuple()))
    else:
        return int((time.mktime(now_time.timetuple()) * 1000))
