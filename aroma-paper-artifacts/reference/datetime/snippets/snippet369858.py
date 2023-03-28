import json
import os
import platform
import time
import traceback
from celery import chord, group
from datetime import datetime
from copy import deepcopy
from atp.api.comm_log import logger
from atp.engine.api_chain import smart_filter_testcase, get_testcase_id_list_filter_by_tag, get_table_data
from atp.engine.api_load_test import ApiTestLoader
from atp.engine.api_report import perfect_summary
from atp.engine.celery_tasks import celery_collect_results, celery_run_single_intf_or_single_main_case, celery_run_debug, celery_run_main_case_list
from atp.httprunner import HttpRunner, logger as hr_logger
from atp.api.mysql_manager import ApiTestcaseInfoManager, ApiRunTaskResultManager, ApiTaskInfoManager, CeleryTaskRecordManager, ApiTestcaseReuseRecordManager, ApiTestcaseMainManager, ApiIntfInfoManager, ApiSystemInfoManager, ApiProductLineManager, GenerateDataRecordManager
from atp.config.default import get_config
from atp.utils.common import read_custom
from atp.utils.tools import json_loads, json_dumps


def set_run_task_result(self, task_id):
    '写入回归任务运行记录'
    self.run_task_result_id = ApiRunTaskResultManager.get_next_result_id()
    start_time = datetime.now()
    ApiRunTaskResultManager.insert_result(id=self.run_task_result_id, api_task_id=task_id, creator=self.executor, start_time=start_time, run_env_id=self.env_id, run_main_case_in_parallel=self.run_main_case_in_parallel)
    self.set_run_task_log_dir()
