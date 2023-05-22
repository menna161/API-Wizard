import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def req_get(url, proxy):
    res_body = ''
    if proxy:
        try:
            res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False, proxies=proxy, timeout=5)
            res.encoding = 'utf-8'
        except:
            print('\x1b[1;31m网络出错！\x1b[0m')
            pass
    else:
        try:
            res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False, timeout=5)
            res.encoding = 'utf-8'
        except:
            print('\x1b[1;31m网络出错！\x1b[0m')
            pass
    return res
