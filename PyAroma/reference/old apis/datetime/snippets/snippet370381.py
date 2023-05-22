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
def get_current_date(fmt='%Y-%m-%d'):
    ' 时间-获取当前日期\n    get current date, default format is %Y-%m-%d\n    :desc: 说明: 获取当前的日期，以%YYYY-%mm-%dd格式返回，例如 2019-09-10\n    '
    return datetime.datetime.now().strftime(fmt)
