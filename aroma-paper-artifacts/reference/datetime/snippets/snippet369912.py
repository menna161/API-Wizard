import functools
import json
import platform
import time
import traceback
from copy import copy, deepcopy
from datetime import datetime
from flask import Blueprint
from flask_restful import Resource
from atp.api.comm_log import logger
from atp.api.disconf_executor import disconf_get_config, edit_disconf_value
from atp.api.excel_parser import ExcelParser
from atp.api.mysql_manager import ApiSystemInfoManager, ApiTaskInfoManager, ApiTestcaseMainManager, ApiTestcaseInfoManager, GitDiffVersionManager, ApiProjectInfoManager, ApiRunTaskResultManager, CeleryTaskRecordManager, ApiIntfInfoManager, EnvInfoManager, TestcaseTagManager
from atp.api.ssh_client import SSHClient
from atp.config.default import get_config
from atp.engine.api_chain import get_table_data, count_testcase_total
from atp.engine.api_runner import ApiRunner
from atp.engine.api_task_result_collector import TaskResultCollector
from atp.engine.return_code_desc import CODE_DESC_MAP
from atp.utils.tools import json_loads, json_dumps, get_current_timestamp, get_current_time
from atp.views.wrappers import timer, login_check, developer_check, master_check
from atp.utils.common import get_request_json, make_response, username_to_nickname, read_custom
from atp.api.redis_api import RedisManager
from flask import request
from atp.api.http_client import HttpClient
from atp.config.load_config import load_config


@login_check
def get_run_result_by_single_day(self):
    '\n            Input:\n            {\n                "companyId": 1,\n                "runDate": "2019-05-13",\n            }\n            Return:\n            {\n                "code": "000",\n                "dataList": [\n                    {\n                        "taskRunId": 1,\n                        "envName": "ALIUAT",\n                        "taskName": "",\n                        "taskType": 1,\n                        "projectName": "项目1",\n                        "totalCaseNum": 100,\n                        "runCaseNum": 100,\n                        "succCaseNum": 90,\n                        "failCaseNum": 10,\n                        "successRate": "90%",\n                        "duration": "10分钟",\n                        "runTime": "2019-04-23 16:00:33",\n                        "executor": "查道庆",\n                    }\n                ]\n            }\n        '
    try:
        company_id = self.data.pop('companyId')
        run_date_str = self.data.pop('runDate')
    except KeyError:
        return make_response({'code': '100', 'desc': CODE_DESC_MAP['100']})
    run_date = datetime.strptime(run_date_str, '%Y-%m-%d')
    res_list = ApiRunTaskResultManager.get_results_by_run_date_in_company(company_id, run_date=run_date)
    res_list_without_project = ApiRunTaskResultManager.get_results_by_run_date_in_company_ignore_project(company_id, run_date=run_date)
    res_list.extend(res_list_without_project)
    date_list = []
    for row in res_list:
        date_list.append({'taskRunId': row[0], 'taskName': row[1], 'taskType': row[2], 'projectName': (row[3] if row[3] else ''), 'totalCaseNum': row[4], 'notRunCaseNum': row[5], 'runCaseNum': row[6], 'succCaseNum': row[7], 'failCaseNum': row[8], 'successRate': calc_success_rate(row[7], row[6]), 'duration': get_duration_msg(row[9], row[10]), 'runTime': format(row[9]), 'executor': row[11], 'envName': row[12]})
    return make_response({'code': '000', 'dataList': date_list})
