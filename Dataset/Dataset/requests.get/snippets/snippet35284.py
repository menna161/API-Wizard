import requests
from urllib import parse
import urllib3
import base64
import argparse
import time
import random
import sys
from bs4 import BeautifulSoup


def proxy_get(host, proxy):
    if proxy:
        proxies = random.choice(proxy)
        proxies_use = {'http': 'http://{}'.format(proxies.strip('\n')), 'https': 'https://{}'.format(proxies.strip('\n'))}
        try:
            res = requests.get(url=host, headers=headers, verify=False, proxies=proxies_use, timeout=5)
            res.encoding = 'utf-8'
            if ((res.status_code == 500) and ('ThinkPHP' in res.text)):
                sta_code = 200
            else:
                sta_code = res.status_code
        except:
            sta_code = 100
        while (sta_code != 200):
            proxy.remove(proxies)
            if proxy:
                proxies = random.choice(proxy)
                proxies_use = {'http': 'http://{}'.format(proxies.strip('\n')), 'https': 'https://{}'.format(proxies.strip('\n'))}
                try:
                    res = requests.get(url=host, headers=headers, verify=False, allow_redirects=False, proxies=proxies_use, timeout=5)
                    sta_code = res.status_code
                except:
                    pass
            else:
                print('没有代理可用了')
                sys.exit(0)
    else:
        proxy = False
        proxies_use = []
    return (proxies_use, proxy)
