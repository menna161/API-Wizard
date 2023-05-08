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


def get_duration_msg(start_time, end_time=None):
    '获取时长文字'
    if (not end_time):
        end_time = datetime.now()
    duration_seconds = (end_time - start_time).seconds
    if (duration_seconds >= 60):
        duration_minutes = int((duration_seconds / 60))
        if (duration_minutes >= 720):
            return '超过12小时未收集到结果'
        delta_seconds = (duration_seconds % 60)
        return '{0}分钟{1}秒'.format(duration_minutes, delta_seconds)
    else:
        return '{}秒'.format(duration_seconds)
