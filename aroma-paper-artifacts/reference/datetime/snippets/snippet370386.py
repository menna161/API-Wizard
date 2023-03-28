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
def get_month_range(change=None):
    ' 时间-获取当前月的总天数 : 增量\n    :desc: 说明: 获取当前月的总天数，加上增量，返回月份的总天数\n    :param change:增量: 增减月份的量，+代表增加，-代表减去，例如: +1代表下个月, -1代表上个月, 0代表当前月\n    '
    change = (int(change) if change else 0)
    dt = (datetime.datetime.now() + relativedelta(months=change))
    month_range = calendar.monthrange(dt.year, dt.month)
    return month_range[1]
