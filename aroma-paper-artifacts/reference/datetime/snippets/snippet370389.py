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
def get_random_member_id(db_connect):
    '\n    :desc:\n    :return:\n    '
    random_sec = random.randint(0, 10000)
    new_last_gen_time = (datetime.datetime.strptime('2017-11-14 17:46:06', '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=random_sec))
    new_last_gen_time = new_last_gen_time.strftime('%Y-%m-%d %H:%M:%S')
    while True:
        return_info = sql_execute('', db_connect=db_connect)
        max_member_id = (return_info[0][0] + 1)
        last_gen_time = return_info[0][1].strftime('%Y-%m-%d %H:%M:%S')
        update_sequence = ('' % (str(max_member_id), new_last_gen_time, last_gen_time))
        return_info = sql_execute(update_sequence, db_connect=db_connect)
        if (return_info == 1):
            break
    return int(max_member_id)
