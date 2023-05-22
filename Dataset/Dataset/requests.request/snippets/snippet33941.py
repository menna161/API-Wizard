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


def _articles(self, cid, pro):
    ' 获取文章列表接口方法 '
    global ALL_ARTICLES
    log.info('请求获取文章列表接口：')
    url = 'https://time.geekbang.org/serv/v1/column/articles'
    method = 'POST'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'time.geekbang.org'
    headers['Origin'] = 'https://time.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    params = {'cid': cid, 'size': 100, 'prev': 0, 'order': 'earliest', 'sample': 'false'}
    log.info(f'接口请求参数：{params}')
    res = requests.request(method, url, headers=headers, json=params)
    if (res.status_code != 200):
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'获取文章列表接口请求出错，返回内容为：{res.json()}')
        raise RequestError(f'获取文章列表接口请求出错，返回内容为：{res.json()}')
    data = res.json().get('data', {})
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    if data:
        ids = []
        article_list = data.get('list', [])
        for article in article_list:
            ids.append(article['id'])
        ALL_ARTICLES += ids
        pro['article_ids'] += ids
    else:
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'获取文章列表接口没有获取到内容，请检查请求。返回结果为：{res.json()}')
        raise NotValueError(f'获取文章列表接口没有获取到内容，请检查请求。返回结果为：{res.json()}')
    log.info(('-' * 40))
