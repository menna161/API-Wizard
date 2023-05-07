from typing import List, Dict
import datetime
import json
from qdata.errors import QdataError, ErrorCode
from . import common


def format_data(data: Dict):
    keyword = str(data['key'])
    start_date = datetime.datetime.strptime(data['startDate'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(data['endDate'], '%Y-%m-%d')
    date_list = []
    while (start_date <= end_date):
        date_list.append(start_date)
        start_date += datetime.timedelta(days=1)
    index_datas = data['data']
    for (i, cur_date) in enumerate(date_list):
        try:
            index_data = index_datas[i]
        except IndexError:
            index_data = ''
        formated_data = {'keyword': [keyword_info['name'] for keyword_info in json.loads(keyword.replace("'", '"'))], 'date': cur_date.strftime('%Y-%m-%d'), 'index': (index_data if index_data else '0')}
        (yield formated_data)
