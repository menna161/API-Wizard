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


def _comments(self, aid):
    ' 获取文章评论详情接口 '
    log.info('请求获取文章评论详情接口：')
    url = 'https://time.geekbang.org/serv/v1/comments'
    method = 'POST'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'time.geekbang.org'
    headers['Origin'] = 'https://time.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    params = {'aid': aid, 'prev': '0'}
    log.info(f'接口请求参数：{params}')
    res = requests.request(method, url, headers=headers, json=params)
    if (res.status_code != 200):
        log.error(f'获取文章评论接口请求出错，返回内容为：{res.content.decode()}')
        return None
    data = res.json().get('data', {}).get('list', [])
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    if data:
        keys = ['comment_content', 'comment_ctime', 'user_header', 'user_name', 'replies']
        comments = [{key: value for (key, value) in comment.items() if (key in keys)} for comment in data]
        return comments
    else:
        return None
