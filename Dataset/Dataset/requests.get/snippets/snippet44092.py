from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def Download(self, downloadUrl, path, isOpenProxy=False, myProxies=None):
    '下载'
    pattern = re.compile('//(.*?)/')
    hostUrl = pattern.findall(downloadUrl)[0]
    self.headers['Host'] = hostUrl
    if isOpenProxy:
        proxies = {'http': ('http://' + myProxies)}
        resp = requests.get(downloadUrl, headers=self.headers, proxies=proxies, timeout=5)
    else:
        resp = requests.get(downloadUrl, headers=self.headers, timeout=5)
    with open(path, 'wb') as fw:
        fw.write(resp.content)
