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


def set_run_task_log_dir(self):
    base_run_task_log_dir = config.RUN_TASK_LOG_DIR
    today_str = datetime.now().strftime('%Y-%m-%d')
    if (platform.system() == 'Windows'):
        self.run_task_log_dir = '{0}{1}\\task_run_{2}\\'.format(base_run_task_log_dir, today_str, self.run_task_result_id)
    else:
        self.run_task_log_dir = '{0}{1}/task_run_{2}/'.format(base_run_task_log_dir, today_str, self.run_task_result_id)
    if (not os.path.exists(self.run_task_log_dir)):
        os.makedirs(self.run_task_log_dir)
