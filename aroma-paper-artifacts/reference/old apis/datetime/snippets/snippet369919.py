import os
import traceback
from datetime import datetime
from atp.api.mysql_manager import ApiRunTaskResultManager, CeleryTaskRecordManager, ApiTaskInfoManager, ApiTestcaseReuseRecordManager
from atp.utils.tools import json_dumps, json_loads
from atp.config.default import Config


def save_task_results(self):
    '保存测试结果到任务运行结果表api_run_task_result和用例复用表api_testcase_reuse_record'
    summary_list = []
    for summary_path in self.summary_path_list:
        if ((not summary_path) or ('worker_summary_path is None' == summary_path)):
            continue
        with open(summary_path, 'r') as f:
            summary_str = f.readline()
            summary_dict = json_loads(summary_str)
            summary_list.append(summary_dict)
            if (not self.run_task_result_id):
                self.run_task_result_id = (summary_dict['run_task_result_id'] if ('run_task_result_id' in summary_dict) else None)
            if (not self.log_dir):
                self.log_dir = (summary_dict['log_dir'] if ('log_dir' in summary_dict) else None)
    with open('{0}task_run_{1}_summary.log'.format(self.log_dir, self.run_task_result_id), 'w') as f:
        f.write(json_dumps(summary_list))
    callback_task_obj = CeleryTaskRecordManager.get_callback_celery(api_run_task_result_id=self.run_task_result_id)
    try:
        CeleryTaskRecordManager.update_celery(callback_task_obj.id, celery_task_status='RUNNING')
        total_cases = 0
        for summary in summary_list:
            total_cases += summary.pop('total_cases')
        res_obj = ApiRunTaskResultManager.get_result(id=self.run_task_result_id)
        task_obj = ApiTaskInfoManager.get_task(id=res_obj.api_task_id)
        if (task_obj.task_type in (1, 3)):
            task_intf_id_list = json_loads(task_obj.case_tree)['intf_id_list']
        else:
            task_intf_id_list = json_loads(task_obj.effect_intf_id_list)
        res_list = save_testcase_reuse_record(summary_list)
        covered_intf_id_set = res_list[0]
        run_cases = res_list[1]
        success_cases = res_list[2]
        uncovered_intf_id_list = list((set(task_intf_id_list) ^ covered_intf_id_set))
        fail_cases = (run_cases - success_cases)
        not_run_cases = (total_cases - run_cases)
        ApiRunTaskResultManager.update_result(self.run_task_result_id, total_cases=total_cases, not_run_cases=not_run_cases, run_cases=run_cases, success_cases=success_cases, fail_cases=fail_cases, end_time=datetime.now(), covered_intf_id_list=json_dumps(list(covered_intf_id_set)), uncovered_intf_id_list=json_dumps(uncovered_intf_id_list))
        CeleryTaskRecordManager.update_celery(callback_task_obj.id, celery_task_status='SUCCESS')
    except Exception as err:
        ApiRunTaskResultManager.update_result(self.run_task_result_id, end_time=datetime.now())
        CeleryTaskRecordManager.update_celery(callback_task_obj.id, celery_task_status='ERROR')
        print('\n'.join([str(err), traceback.format_exc()]))
        raise Exception(err)
