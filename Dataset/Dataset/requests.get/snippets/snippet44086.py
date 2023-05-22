from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def GetHtml(self, url, isOpenProxy=False, myProxies=None):
    '\n        获取Html页面\n        :param isOpenProxy: 是否打开代理，默认否\n        :param Proxies: 代理ip和端口，例如：103.109.58.242:8080，默认无\n        :return:\n        '
    try:
        pattern = re.compile('//(.*?)/')
        hostUrl = pattern.findall(url)[0]
        self.headers['Host'] = hostUrl
        if isOpenProxy:
            proxies = {'http': ('http://' + myProxies)}
            resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=5)
        else:
            resp = requests.get(url, headers=self.headers, timeout=5)
        resp.encoding = resp.apparent_encoding
        print(('GetHtml成功...' + url))
        return resp
    except Exception as e:
        print(('GetHtml失败...' + url))
        print(e)
