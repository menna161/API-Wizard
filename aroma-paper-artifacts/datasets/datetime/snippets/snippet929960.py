from typing import List, Dict
import datetime
import json
from . import common
from qdata.errors import QdataError, ErrorCode


def format_data(data: Dict):
    '\n        格式化堆在一起的数据\n    '
    keyword = str(data['word'])
    start_date = datetime.datetime.strptime(data['all']['startDate'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(data['all']['endDate'], '%Y-%m-%d')
    date_list = []
    while (start_date <= end_date):
        date_list.append(start_date)
        start_date += datetime.timedelta(days=1)
    for kind in ALL_KIND:
        index_datas = data[kind]['data']
        for (i, cur_date) in enumerate(date_list):
            try:
                index_data = index_datas[i]
            except IndexError:
                index_data = ''
            formated_data = {'keyword': [keyword_info['name'] for keyword_info in json.loads(keyword.replace("'", '"'))], 'type': kind, 'date': cur_date.strftime('%Y-%m-%d'), 'index': (index_data if index_data else '0')}
            (yield formated_data)
