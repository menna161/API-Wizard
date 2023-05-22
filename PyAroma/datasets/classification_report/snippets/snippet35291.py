import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def check_dubug(host):
    fo = open('{}.txt'.format(parse.urlparse(host).hostname), 'a')
    headers['Host'] = parse.urlparse(host).hostname
    div_html_5 = ''
    div_html_3 = ''
    print('\x1b[1;34m[+] 检测Debug模式是否开启: \x1b[0m')
    debug_bool = False
    url_debug = ['indx.php', '/index.php/?s=index/inex/']
    for i in url_debug:
        try:
            res_debug = requests.get(url=(host + i), headers=headers, timeout=5, verify=False, allow_redirects=False)
            res_debug.encoding = 'utf-8'
            if (('Environment Variables' in res_debug.text) or ('错误位置' in res_debug.text)):
                print('\x1b[1;32m[+] Debug 模式已开启！\x1b[0m')
                debug_bool = True
                res_debug_html = BeautifulSoup(res_debug.text, 'html.parser')
                div_html_5 = res_debug_html.findAll('div', {'class': 'clearfix'})
                div_html_3 = res_debug_html.find('sup')
                div_html_3_path = res_debug_html('div', {'class': 'text'})
                break
        except:
            print('\x1b[1;31m[+] 检测出错\x1b[0m')
    if (debug_bool == False):
        print('\x1b[1;31m[+] Debug 模式未开启！\x1b[0m')
    if debug_bool:
        if div_html_5:
            for j in div_html_5:
                if (j.strong.text == 'THINK_VERSION'):
                    fo.write('ThinkPHP Version: {}\n'.format(j.small.text.strip()))
                    print('\x1b[1;32m[+] ThinkPHP Version: {}\x1b[0m'.format(j.small.text.strip()))
                if (j.strong.text == 'DOCUMENT_ROOT'):
                    fo.write('DOCUMENT ROOT: {}\n'.format(j.small.text.strip()))
                    print('\x1b[1;32m[+] DOCUMENT ROOT: {}\x1b[0m'.format(j.small.text.strip()))
                if (j.strong.text == 'SERVER_ADDR'):
                    fo.write('SERVER ADDR: {}\n'.format(j.small.text.strip()))
                    print('\x1b[1;32m[+] SERVER ADDR: {}\x1b[0m'.format(j.small.text.strip()))
                if (j.strong.text == 'LOG_PATH'):
                    fo.write('LOG PATH: {}\n'.format(j.small.text.strip()))
                    print('\x1b[1;32m[+] LOG PATH: {}\x1b[0m'.format(j.small.text.strip()))
        elif (div_html_3 and div_html_3_path):
            fo.write('ThinkPHP Version: {}\n'.format(div_html_3.text))
            fo.write('ThinkPHP Path: {}\n'.format(div_html_3_path[0].p.text))
            print('\x1b[1;32m[+] ThinkPHP Version: {}\x1b[0m'.format(div_html_3.text))
            print('\x1b[1;32m[+] ThinkPHP Path: {}\x1b[0m'.format(div_html_3_path[0].p.text))
    fo.close()
