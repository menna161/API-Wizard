import pika
import time
import os
import platform
from datetime import datetime
from copy import copy
import re
from atp.config.load_config import load_config
from atp.utils.tools import get_current_timestamp


def push_debug_log(self):
    '推log'
    print('进入push_log')
    count = 0
    today_str = datetime.now().strftime('%Y-%m-%d')
    if (platform.system() == 'Windows'):
        log_dir = '{0}{1}\\'.format(self.run_case_log_dir, today_str)
    else:
        log_dir = '{0}{1}/'.format(self.run_case_log_dir, today_str)
    g = self._create_generator('{dir}run_{report_id}.log'.format(dir=log_dir, report_id=self.report_id))
    end_flag = False
    current_case = None
    for i in g:
        count += 1
        if end_flag:
            break
        time.sleep(0.5)
        if isinstance(i, list):
            p_list = []
            for p in i:
                if p.startswith('[{}-'.format(_YEAR)):
                    p = (p[:33] + p[39:])
                p = p.replace(' ', '&nbsp')
                res = color_log(p, current_case)
                if (not isinstance(res, str)):
                    p = res[0]
                    current_case = res[1]
                else:
                    p = res
                p = font_log(p)
                p_list.append(p)
                if ('【END】' in p):
                    end_flag = True
            if p_list:
                ps = '<br/>'.join(p_list)
                self.send_single_message(ps)
        else:
            print('i 是 {}'.format(type(i)))
            i = i.replace(' ', '&nbsp')
            count += 1
            self.send_single_message(i)
            if ('【END】测试结束' in i):
                break
