import time
import datetime
import requests
import re
from copy import deepcopy
import logging
import os
import pathlib
import traceback
import sys


def _login(self):
    ' 登录接口方法 '
    log.info('请求登录接口：')
    url = 'https://account.geekbang.org/account/ticket/login'
    method = 'POST'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'account.geekbang.org'
    headers['Origin'] = 'https://account.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    params = {'country': 86, 'cellphone': self.cellphone, 'password': self.password, 'captcha': '', 'remember': 1, 'platform': 3, 'appid': 1, 'source': ''}
    log.info(f'接口请求参数：{params}')
    res = requests.request(method, url, headers=headers, json=params)
    if ((res.status_code != 200) or (str(res.json().get('code', '')) == '-1')):
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'登录接口请求出错，返回内容为：{res.content.decode()}')
        raise RequestError(f'登录接口请求出错，返回内容为：{res.content.decode()}')
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    log.info(('-' * 40))
