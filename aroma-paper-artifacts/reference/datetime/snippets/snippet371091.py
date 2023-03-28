import json
from datetime import datetime, timedelta
from flask import Blueprint, request
from flask_restful import Resource
from atp.api.comm_log import logger
from atp.engine.return_code_desc import CODE_DESC_MAP
from atp.utils.tools import json_dumps, json_loads
from atp.views.wrappers import timer, login_check, developer_check
from atp.utils.common import get_request_json, make_response, username_to_nickname
from atp.api.mysql_manager import stat_api_testcase, ApiTestcaseInfoManager, get_reuse_group_by_testcase_id, ApiCompanyInfoManager, ApiSystemInfoManager, get_reuse_group_by_intf_id, get_reuse_group_by_system_id, get_reuse_group_by_day, get_reuse_group_by_month, get_reuse_group_by_week
from atp.api.redis_api import RedisManager


def get_reuse_summary(self):
    '\n        查询用例复用记录汇总\n        Input:\n            {   #三选一必填\n                "companyId": 1,\n                "systemId": 1,\n                "intfId": 1,\n                "recentDays": 30  #非必填\n            }\n        Return:\n            {\n                "code": "000",\n                "valueList": [\n                    {\n                        "labelName": "",\n                        "totalReuseNum": 0,\n                        "succReuseNum": 0,\n                        "failReuseNum": 0,\n                        "succRate": "100%"\n                    }\n                ]\n            }\n\n        '
    try:
        company_id = self.data.pop('companyId', None)
        system_id = self.data.pop('systemId', None)
        intf_id = self.data.pop('intfId', None)
        recent_days = self.data.pop('recentDays', None)
        if (not (company_id or intf_id or system_id)):
            raise KeyError
    except KeyError:
        return make_response({'code': '100', 'desc': CODE_DESC_MAP['100']})
    today_date = datetime.date(datetime.now())
    if recent_days:
        start_day = (today_date + timedelta(days=(- int(recent_days))))
    else:
        start_day = datetime.fromtimestamp(1555516800)
    value_list = []
    res_list = []
    if intf_id:
        res_list = get_reuse_group_by_testcase_id(start_day, today_date, intf_id)
    elif system_id:
        res_list = get_reuse_group_by_intf_id(start_day, today_date, system_id)
    elif company_id:
        res_list = get_reuse_group_by_system_id(start_day, today_date, company_id)
    for row in res_list:
        value_list.append({'labelName': row[1], 'totalReuseNum': int(row[2]), 'succReuseNum': int(row[3]), 'failReuseNum': int(row[4]), 'succRate': calc_success_rate(int(row[3]), int(row[2]))})
    bubble_sort_by_total(value_list)
    return make_response({'code': '000', 'valueList': value_list})
