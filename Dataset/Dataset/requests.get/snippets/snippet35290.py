import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def log_find(host):
    fo = open('{}.txt'.format(parse.urlparse(host).hostname), 'a')
    headers['Host'] = parse.urlparse(host).hostname
    print('\x1b[1;34m[!] 日志文件路径探测：\x1b[0m')
    time_dir_5 = time.strftime('%Y%m/%d', time.localtime())
    log_dir_info_5 = (host + '/../../runtime/log/{}.log'.format(time_dir_5))
    log_dir_error_5 = (host + '/../../runtime/log/{}_error.log'.format(time_dir_5))
    log_dir_sql_5 = (host + '/../../runtime/log/{}_sql.log'.format(time_dir_5))
    try:
        info_res = requests.get(url=log_dir_info_5, headers=headers, timeout=5, verify=False, allow_redirects=False)
        error_res = requests.get(url=log_dir_error_5, headers=headers, timeout=5, verify=False, allow_redirects=False)
        sql_res = requests.get(url=log_dir_sql_5, headers=headers, timeout=5, verify=False, allow_redirects=False)
        if ((info_res.status_code == 200) and (('[ info ]' in info_res.text) or ('[ sql ]' in info_res.text) or ('[ error ]' in info_res.text))):
            fo.write('info日志存在: {}\n'.format(log_dir_info_5))
            print(('\x1b[1;32m[+] info日志存在: \x1b[0m' + log_dir_info_5))
        if ((error_res.status_code == 200) and (('[ info ]' in error_res.text) or ('[ sql ]' in error_res.text) or ('[ error ]' in error_res.text))):
            fo.write('error日志存在: {}\n'.format(log_dir_error_5))
            print(('\x1b[1;32m[+] error日志存在: \x1b[0m' + log_dir_error_5))
        if ((sql_res.status_code == 200) and (('[ info ]' in sql_res.text) or ('[ sql ]' in sql_res.text) or ('[ error ]' in sql_res.text))):
            fo.write('sql日志存在: {}\n'.format(log_dir_sql_5))
            print(('\x1b[1;32m[+] sql日志存在: \x1b[0m' + log_dir_sql_5))
    except:
        print('\x1b[1;31m网络出错！\x1b[0m')
    time_dir_3 = time.strftime('%y_%m_%d', time.localtime())
    log_dir_3_1 = (host + '/Application/Runtime/Logs/Home/{}.log'.format(time_dir_3))
    log_dir_3_2 = (host + '/Runtime/Logs/Home/{}.log'.format(time_dir_3))
    log_dir_3_3 = (host + '/Runtime/Logs/Common/{}.log'.format(time_dir_3))
    log_dir_3_4 = (host + '/Application/Runtime/Logs/Common/{}.log'.format(time_dir_3))
    log_dir_3_5 = (host + '/App/Runtime/Logs/Home/{}.log'.format(time_dir_3))
    log_dir_3 = [log_dir_3_1, log_dir_3_2, log_dir_3_3, log_dir_3_4, log_dir_3_5]
    for i in log_dir_3:
        try:
            log_3_res = requests.get(url=i, headers=headers, timeout=5, verify=False, allow_redirects=False)
            log_3_res.encoding = 'utf-8'
            if ((log_3_res.status_code == 200) and (('INFO:' in log_3_res.text) or ('SQL语句' in log_3_res.text) or ('ERR:' in log_3_res.text))):
                fo.write('日志存在: {}\n'.format(i))
                print(('\x1b[1;32m[+] 日志存在: \x1b[0m' + i))
            else:
                pass
        except:
            print('\x1b[1;31m网络出错！\x1b[0m')
    fo.close()
