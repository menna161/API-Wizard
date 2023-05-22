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


def _product(self, _type='c1'):
    ' 商品列表（就是课程）的接口）方法 '
    log.info('请求获取课程列表接口：')
    url = 'https://time.geekbang.org/serv/v3/learn/product'
    method = 'POST'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'time.geekbang.org'
    headers['Origin'] = 'https://time.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    params = {'desc': 'true', 'expire': 1, 'last_learn': 0, 'learn_status': 0, 'prev': 0, 'size': 20, 'sort': 1, 'type': '', 'with_learn_count': 1}
    log.info(f'接口请求参数：{params}')
    res = requests.request(method, url, headers=headers, json=params)
    if (res.status_code != 200):
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'课程列表接口请求出错，返回内容为：{res.content.decode()}')
        raise RequestError(f'课程列表接口请求出错，返回内容为：{res.content.decode()}')
    data = res.json().get('data', {})
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    if data:
        self.products += self._parser_products(data, _type)
    else:
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'课程列表接口没有获取到内容，请检查请求。返回结果为：{res.content.decode()}')
        raise NotValueError(f'课程列表接口没有获取到内容，请检查请求。返回结果为：{res.content.decode()}')
    log.info(('-' * 40))
