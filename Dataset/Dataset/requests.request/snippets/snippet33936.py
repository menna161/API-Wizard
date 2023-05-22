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


def _user_auth(self):
    ' 用户认证接口方法 '
    log.info('请求用户认证接口：')
    now_time = int((time.time() * 1000))
    url = f'https://account.geekbang.org/serv/v1/user/auth?t={now_time}'
    method = 'GET'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'account.geekbang.org'
    headers['Origin'] = 'https://time.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    res = requests.request(method, url, headers=headers)
    if ((res.status_code != 200) or (str(res.json().get('code', '')) != '0')):
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'用户认证接口请求出错，返回内容为：{res.json()}')
        raise RequestError(f'用户认证接口请求出错，返回内容为：{res.json()}')
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    log.info(('-' * 40))
