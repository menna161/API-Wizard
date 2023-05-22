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


def _article(self, aid, pro, file_type=None, get_comments=False):
    ' 通过课程 ID 获取文章信息接口方法 '
    global FINISH_ARTICLES
    log.info('请求获取文章信息接口：')
    url = 'https://time.geekbang.org/serv/v1/article'
    method = 'POST'
    headers = deepcopy(self.common_headers)
    headers['Host'] = 'time.geekbang.org'
    headers['Origin'] = 'https://time.geekbang.org'
    headers['Cookie'] = self.cookie.cookie_string
    params = {'id': aid, 'include_neighbors': 'true', 'is_freelyread': 'true'}
    log.info(f'接口请求参数：{params}')
    res = requests.request(method, url, headers=headers, json=params)
    if (res.status_code != 200):
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'获取文章信息接口请求出错，返回内容为：{res.content.decode()}')
        raise RequestError(f'获取文章信息接口请求出错，返回内容为：{res.content.decode()}')
    data = res.json().get('data', {})
    self.cookie.load_set_cookie(res.headers['Set-Cookie'])
    if data:
        comments = (self._comments(aid) if get_comments else None)
        keys = ['article_content', 'article_title', 'id', 'audio_download_url']
        article = {key: value for (key, value) in data.items() if (key in keys)}
        self.save_to_file(pro['title'], article['article_title'], article['article_content'], audio=article['audio_download_url'], file_type=file_type, comments=comments)
        FINISH_ARTICLES.append(article['id'])
        pro['cid'] = data['cid']
    else:
        _save_finish_article_id_to_file()
        log.info(f'此时 products 的数据为：{self.products}')
        log.error(f'获取文章信息接口没有获取到内容，请检查请求。返回结果为：{res.content.decode()}')
        raise NotValueError(f'获取文章信息接口没有获取到内容，请检查请求。返回结果为：{res.content.decode()}')
    log.info(('-' * 40))
