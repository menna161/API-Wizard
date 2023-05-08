import json
from datetime import datetime, timedelta
from flask import Blueprint, request
from flask_restful import Resource
from atp.api.comm_log import logger
from atp.api.mysql_manager import ApiCompanyInfoManager, ApiSystemInfoManager, ApiProductLineManager, ApiTestcaseMainManager, ApiTestcaseSubManager
from atp.api.redis_api import RedisManager
from atp.engine.return_code_desc import CODE_DESC_MAP
from atp.utils.common import get_request_json, make_response, db_result_to_map
from atp.views.wrappers import timer, login_check, master_check, developer_check


@login_check
def project_subtree(self):
    '根据公司id查询配置在该公司下的项目-系统-接口-用例'
    try:
        company_id = self.data.pop('companyId')
        recent_days = int(self.data.pop('recentDays', 0))
    except (KeyError, ValueError):
        return make_response({'code': '100', 'desc': '入参校验失败'})
    if recent_days:
        today_date = datetime.date(datetime.now())
        start_day = (today_date + timedelta(days=(- int(recent_days))))
        result_list = self.acim.query_api_project_subtree(company_id, start_day=start_day)
    else:
        result_list = self.acim.query_api_project_subtree(company_id)
    patch_result_list = self.acim.query_api_project_subtree_patch(company_id)
    subtree = result_list_to_subtree(result_list, patch_result_list)
    return make_response({'code': '000', 'data': subtree})
