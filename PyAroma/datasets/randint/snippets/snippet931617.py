import os
import json
import re
import time
import getopt
import sys
import queue as Queue
from random import randrange
from random import randint
from requests_html import HTMLSession
from threading import Thread
from local_file_adapter import LocalFileAdapter


def get_list_by_uid(user_id, dytk, cursor=0, favorite=False):
    '获取用户视频列表信息\n\n    @param: user_id\n    @param: dytk\n    @param: cursor,用于列表分页定位\n    @return json\n    '
    global FREEZE_SIGNATURE
    '读取数据文件,若存在则直接返回'
    file_result = load_from_json_file(user_id, cursor, favorite)
    if file_result:
        return file_result
    if favorite:
        url = LIKE_LIST_URL
    else:
        url = POST_LIST_URL
    '获取签名'
    signature = (FREEZE_SIGNATURE if FREEZE_SIGNATURE else get_signature(user_id))
    headers = {**DOWNLOAD_HEADERS, 'x-requested-with': 'XMLHttpRequest', 'accept': 'application/json'}
    params = {'user_id': user_id, 'count': 30, 'max_cursor': cursor, 'app_id': 1128, '_signature': signature}
    with HTMLSession() as session:
        while True:
            r = session.get(url, params=params, headers=headers)
            if (r.status_code != 200):
                print(r)
                continue
            r.html.render()
            res_json = json.loads(r.html.text)
            r.close()
            if res_json.get('max_cursor', None):
                FREEZE_SIGNATURE = signature
                save_json_data(user_id, cursor, res_json, favorite)
                return res_json
            print(('get empty list, ' + str(res_json)))
            time.sleep(randint(1, 5))
            print('retry...')
