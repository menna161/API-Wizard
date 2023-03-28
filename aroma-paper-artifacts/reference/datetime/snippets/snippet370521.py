import json
from datetime import datetime
from atp.api.excel_parser import ExcelParser
from atp.api.mysql_manager import ApiTestcaseInfoManager, ApiTestcaseRequestManager, ApiTestcaseTagRelationManager, UserManager, ApiProjectIntfRelationManager, ApiTestcaseReuseRecordManager
from atp.utils.tools import get_current_time
from atp.views.wrappers import custom_func_wrapper
from atp.app import create_app


def get_duration(create_time, last_modify_time):
    if last_modify_time:
        last_time = last_modify_time
    else:
        last_time = create_time
    today = get_current_time(time_format='%Y-%m-%d')
    d1_list = [int(i) for i in today.split('-')]
    d1 = datetime(d1_list[0], d1_list[1], d1_list[2])
    d2_list = [int(i) for i in format(last_time).split(' ')[0].split('-')]
    d2 = datetime(d2_list[0], d2_list[1], d2_list[2])
    return (d1 - d2).days
