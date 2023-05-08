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


def get_reuse_trend(self):
    '\n        查询用例复用记录变化趋势\n        Input:\n            {   #三选一必填\n                "companyId": 1,\n                "systemId": 1,\n                "intfId": 1,\n                "period": "day"/"week"/"month",\n                "startTimestamp": 1555689600,\n                "endTimestamp": 1557476277,\n            }\n        Return:\n            {\n                "code": "000",\n                "valueList": [\n                    {\n                        "labelName": "",\n                        "totalReuseNum": 0,\n                        "succReuseNum": 0,\n                        "failReuseNum": 0,\n                        "succRate": "100%"\n                    }\n                ]\n            }\n        '
    try:
        company_id = self.data.pop('companyId', None)
        system_id = self.data.pop('systemId', None)
        intf_id = self.data.pop('intfId', None)
        period = self.data.pop('period')
        start_timestamp = self.data.pop('startTimestamp')
        end_timestamp = self.data.pop('endTimestamp')
        if (not (company_id or intf_id or system_id)):
            raise KeyError
    except KeyError:
        return make_response({'code': '100', 'desc': CODE_DESC_MAP['100']})
    start_day = datetime.fromtimestamp(start_timestamp)
    end_day = datetime.fromtimestamp(end_timestamp)
    res_list = []
    value_list = []
    if (period == 'day'):
        res_list = get_reuse_group_by_day(start_day, end_day, intf_id=intf_id, system_id=system_id, company_id=company_id)
    elif (period == 'week'):
        res_list = get_reuse_group_by_week(start_day, end_day, intf_id=intf_id, system_id=system_id, company_id=company_id)
    elif (period == 'month'):
        res_list = get_reuse_group_by_month(start_day, end_day, intf_id=intf_id, system_id=system_id, company_id=company_id)
    for row in res_list:
        value_list.append({'labelName': format(row[0]), 'totalReuseNum': int(row[1]), 'succReuseNum': int(row[2]), 'failReuseNum': int(row[3]), 'succRate': calc_success_rate(int(row[2]), int(row[1]))})
    return make_response({'code': '000', 'valueList': value_list})
