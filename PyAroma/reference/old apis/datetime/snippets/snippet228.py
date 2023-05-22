import datetime
import prettytable
import config.stations as stations
from config.url_config import URLS
from util.net_util import api, save_cookie
from config.stations import get_by_name
from util.app_util import current_date, url_encode
import ticket_config as config


@staticmethod
def search_stack(from_station, to_station, train_date=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'), purpose='ADULT', train_no=None):
    '查询车票'
    url = URLS.get('ticket_query').get('request_url').format(train_date, stations.get_by_name(from_station), stations.get_by_name(to_station), purpose)
    cookies = {'_jc_save_fromDate': config.DATE, '_jc_save_fromStation': url_encode(((config.FROM_STATION + ',') + get_by_name(config.FROM_STATION))), '_jc_save_toDate': current_date(), '_jc_save_toStation': url_encode(((config.TO_STATION + ',') + get_by_name(config.TO_STATION))), '_jc_save_wfdc_flag': 'dc'}
    while True:
        response_search = api.single_get(url, cookies=cookies).json()
        if (not response_search['status']):
            word = response_search['c_url'][11:]
            text = url[(url.rfind('/') + 1):url.find('?')]
            url = url.replace(text, word)
        elif (response_search['status'] and (response_search['httpstatus'] == 200)):
            break
    result = response_search['data']['result']
    return Ticket.decode_data(result, train_no, purpose)
