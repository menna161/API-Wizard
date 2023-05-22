import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def req_post(url, proxy, data):
    res_body = ''
    if proxy:
        try:
            res = requests.post(url=url, headers=headers, verify=False, data=data, allow_redirects=False, proxies=proxy, timeout=5)
            res.encoding = 'utf-8'
        except:
            print('\x1b[1;31m网络出错！\x1b[0m')
            pass
    else:
        try:
            res = requests.post(url=url, headers=headers, verify=False, data=data, allow_redirects=False, timeout=5)
            res.encoding = 'utf-8'
        except:
            print('\x1b[1;31m网络出错！\x1b[0m')
            pass
    return res
