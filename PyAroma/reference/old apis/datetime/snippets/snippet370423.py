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
def setup_fund_order_conf(args, db_connect):
    ' 数据库-配置资金方匹配规则 : 规则参数\n    :desc: 说明: 写入capital.conf_order_fund表，设置资金方匹配规则\n    :param args: 规则参数: 例如 {"idNo":"$ID_NO","applyAmount":"$applyAmount","termNo":"$termValue","repaymentWay":"554","fund":"$fund_id"}\n    :return:\n    '
    id_no = args['idNo']
    order_amount = args['applyAmount']
    term_no = args['termNo']
    repayment_way = args['repaymentWay']
    fund = args['fund']
    industry_type = args.pop('industry_type', None)
    is_accept_unclear = args.pop('is_accept_unclear', None)
    fund_level = args.pop('fund_level', None)
    product_type = args.pop('productType', 0)
    sql_user_age = ''.format(id_no=id_no)
    user_age = sql_execute(sql_user_age, db_connect=db_connect)
    max_user_age = user_age[0][0]
    min_user_age = user_age[0][1]
    min_id = ''
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    industry_type = (industry_type if industry_type else '100013')
    is_accept_unclear = (is_accept_unclear if is_accept_unclear else '10')
    fund_level = (fund_level if fund_level else '0')
    sql_check_unique = ''.format(term_no=term_no, order_amount=order_amount, fund_level=fund_level, repayment_way=repayment_way, fund=fund)
    res = sql_execute(sql_check_unique, db_connect=db_connect)
    if (res[0][0] > 0):
        return (True, '已有相同资金方匹配规则, 未新写入规则')
    sql_fund_order_conf = ''.format(min_id=min_id, order_amount=order_amount, min_user_age=min_user_age, max_user_age=max_user_age, term_no=term_no, repayment_way=repayment_way, fund=fund, create_time=now_time, industry_type=industry_type, is_accept_unclear=is_accept_unclear, fund_level=fund_level, product_type=product_type)
    sql_execute(sql_fund_order_conf, db_connect=db_connect)
