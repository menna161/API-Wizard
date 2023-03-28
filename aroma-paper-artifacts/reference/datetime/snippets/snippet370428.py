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
def setup_qa_create_accounting_overdue(loan_id, overdue_days, env_name):
    ' 其他-根据偏移天数更新贷款数据 : 贷款编号, 偏移天数\n    :param loan_id: 贷款编号:贷款编号loan_id\n    :param overdue_days: 偏移天数:正整数-期望逾期的天数；负数-期望往前偏移的天数\n    :param env_name: 环境名称\n    :return:\n    '
    if (not isinstance(overdue_days, int)):
        raise Exception('偏移天数输入有误，只支持数字')
    if (overdue_days < 0):
        dt = (datetime.datetime.now() + relativedelta(days=overdue_days))
    else:
        dt = ((datetime.datetime.now() + relativedelta(days=(- overdue_days))) + relativedelta(months=(- 1)))
    loan_timestamp = int(time.mktime(dt.timetuple()))
    data = {'env': env_name, 'loanDate': loan_timestamp, 'loanId': loan_id}
    url = 'http://****/atp/qa/createAccountingOverdue'
    header_info = {'Content-Type': 'application/json'}
    hc = HttpClient()
    try:
        r = hc.http_post(url, header_info, data)
        r_dic = json_loads(r.text)
    except Exception as err:
        raise Exception('出现未知错误：{0}'.format(repr(err)))
    if (r_dic['code'] == '000'):
        return True
    else:
        raise Exception(r_dic['desc'])
