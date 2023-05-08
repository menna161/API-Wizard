import os
import traceback
from datetime import datetime
from atp.api.mysql_manager import ApiRunTaskResultManager, CeleryTaskRecordManager, ApiTaskInfoManager, ApiTestcaseReuseRecordManager
from atp.utils.tools import json_dumps, json_loads
from atp.config.default import Config


def save_testcase_reuse_record(summary_list):
    '根据summary_list记录用例复用表，获取覆盖的接口列表、运行的用例数，成功的用例数'
    today_date = datetime.date(datetime.now())
    covered_intf_id_set = set()
    run_cases = 0
    success_cases = 0
    for summary in summary_list:
        if ('summary' not in summary):
            continue
        run_cases += summary['summary']['stat']['testsRun']
        for detail_dic in summary['summary']['details']:
            is_case_success = False
            if (detail_dic['stat']['testsRun'] == detail_dic['stat']['successes']):
                success_cases += 1
                is_case_success = True
            testcase_id = detail_dic['case_id']
            is_main = detail_dic['is_main']
            if is_main:
                been_setup_testcase_id = 0
                reuse_obj = ApiTestcaseReuseRecordManager.get_record(record_date=today_date, api_testcase_main_id=testcase_id, is_setup=0, been_setup_testcase_id=been_setup_testcase_id)
                plus_success_times = (1 if is_case_success else 0)
                plus_fail_times = (0 if is_case_success else 1)
                if (not reuse_obj):
                    ApiTestcaseReuseRecordManager.insert_record(record_date=today_date, api_testcase_main_id=testcase_id, total_times=1, success_times=plus_success_times, fail_times=plus_fail_times, is_setup=0, been_setup_testcase_id=been_setup_testcase_id)
                else:
                    ApiTestcaseReuseRecordManager.update_record(reuse_obj.id, total_times=(reuse_obj.total_times + 1), success_times=(reuse_obj.success_times + plus_success_times), fail_times=(reuse_obj.fail_times + plus_fail_times))
            else:
                covered_intf_id_set.add(detail_dic['intf_id'])
                last_step_main_i = 1
                for record_dic in detail_dic['records']:
                    is_step_success = (True if (record_dic['status'] == 'success') else False)
                    plus_success_times = (1 if is_step_success else 0)
                    plus_fail_times = (0 if is_step_success else 1)
                    step_case_id = record_dic['case_id']
                    if isinstance(step_case_id, int):
                        is_setup = (0 if (step_case_id == testcase_id) else 1)
                        been_setup_testcase_id = (testcase_id if is_setup else 0)
                        reuse_obj = ApiTestcaseReuseRecordManager.get_record(record_date=today_date, api_testcase_id=step_case_id, is_setup=is_setup, been_setup_testcase_id=been_setup_testcase_id)
                        if (not reuse_obj):
                            ApiTestcaseReuseRecordManager.insert_record(record_date=today_date, api_testcase_id=step_case_id, total_times=1, success_times=plus_success_times, fail_times=plus_fail_times, is_setup=is_setup, been_setup_testcase_id=been_setup_testcase_id)
                        else:
                            ApiTestcaseReuseRecordManager.update_record(reuse_obj.id, total_times=(reuse_obj.total_times + 1), success_times=(reuse_obj.success_times + plus_success_times), fail_times=(reuse_obj.fail_times + plus_fail_times))
                    else:
                        (step_main_case_id, step_main_i) = [int(x) for x in str(step_case_id).split('-', maxsplit=1)]
                        if (step_main_i > last_step_main_i):
                            continue
                        is_setup = 1
                        been_setup_testcase_id = testcase_id
                        reuse_obj = ApiTestcaseReuseRecordManager.get_record(record_date=today_date, api_testcase_main_id=step_main_case_id, is_setup=is_setup, been_setup_testcase_id=been_setup_testcase_id)
                        if (not reuse_obj):
                            ApiTestcaseReuseRecordManager.insert_record(record_date=today_date, api_testcase_main_id=step_main_case_id, total_times=1, success_times=plus_success_times, fail_times=plus_fail_times, is_setup=is_setup, been_setup_testcase_id=been_setup_testcase_id)
                        else:
                            ApiTestcaseReuseRecordManager.update_record(reuse_obj.id, total_times=(reuse_obj.total_times + 1), success_times=(reuse_obj.success_times + plus_success_times), fail_times=(reuse_obj.fail_times + plus_fail_times))
                        last_step_main_i = step_main_i
    return (covered_intf_id_set, run_cases, success_cases)
