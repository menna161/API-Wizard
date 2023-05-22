import json
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from tushare.futures import domestic_cons as ct
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError
from http.client import IncompleteRead
from urllib import urlencode
from urllib2 import urlopen, Request
from urllib2 import HTTPError
from httplib import IncompleteRead


def get_dce_daily(date=None, type='future', retries=0):
    "\n        获取大连商品交易所日交易数据\n    Parameters\n    ------\n        date: 日期 format：YYYY-MM-DD 或 YYYYMMDD 或 datetime.date对象 为空时为当天\n        type: 数据类型, 为'future'期货 或 'option'期权二者之一\n        retries: int, 当前重试次数，达到3次则获取数据失败\n    Return\n    -------\n        DataFrame\n            大商所日交易数据(DataFrame):\n                symbol        合约代码\n                date          日期\n                open          开盘价\n                high          最高价\n                low           最低价\n                close         收盘价\n                volume        成交量\n                open_interest   持仓量\n                turnover       成交额\n                settle        结算价\n                pre_settle    前结算价\n                variety       合约类别\n        或 \n        DataFrame\n           郑商所每日期权交易数据\n                symbol        合约代码\n                date          日期\n                open          开盘价\n                high          最高价\n                low           最低价\n                close         收盘价\n                pre_settle      前结算价\n                settle         结算价\n                delta          对冲值  \n                volume         成交量\n                open_interest     持仓量\n                oi_change       持仓变化\n                turnover        成交额\n                implied_volatility 隐含波动率\n                exercise_volume   行权量\n                variety        合约类别\n        或 None(给定日期没有交易数据)\n    "
    day = (ct.convert_date(date) if (date is not None) else datetime.date.today())
    if (retries > 3):
        print('maximum retires for DCE market data: ', day.strftime('%Y%m%d'))
        return
    if (type == 'future'):
        url = ((ct.DCE_DAILY_URL + '?') + urlencode({'currDate': day.strftime('%Y%m%d'), 'year': day.strftime('%Y'), 'month': str((int(day.strftime('%m')) - 1)), 'day': day.strftime('%d')}))
        listed_columns = ct.DCE_COLUMNS
        output_columns = ct.OUTPUT_COLUMNS
    elif (type == 'option'):
        url = ((ct.DCE_DAILY_URL + '?') + urlencode({'currDate': day.strftime('%Y%m%d'), 'year': day.strftime('%Y'), 'month': str((int(day.strftime('%m')) - 1)), 'day': day.strftime('%d'), 'dayQuotes.trade_type': '1'}))
        listed_columns = ct.DCE_OPTION_COLUMNS
        output_columns = ct.OPTION_OUTPUT_COLUMNS
    else:
        print((('invalid type :' + type) + ', should be one of "future" or "option"'))
        return
    try:
        response = urlopen(Request(url, method='POST', headers=ct.DCE_HEADERS)).read().decode('utf8')
    except IncompleteRead as reason:
        return get_dce_daily(day, retries=(retries + 1))
    except HTTPError as reason:
        if (reason.code == 504):
            return get_dce_daily(day, retries=(retries + 1))
        elif (reason.code != 404):
            print(ct.DCE_DAILY_URL, reason)
        return
    if (u'错误：您所请求的网址（URL）无法获取' in response):
        return get_dce_daily(day, retries=(retries + 1))
    elif (u'暂无数据' in response):
        return
    data = BeautifulSoup(response, 'html.parser').find_all('tr')
    if (len(data) == 0):
        return
    dict_data = list()
    implied_data = list()
    for idata in data[1:]:
        if ((u'小计' in idata.text) or (u'总计' in idata.text)):
            continue
        x = idata.find_all('td')
        if (type == 'future'):
            row_dict = {'variety': ct.DCE_MAP[x[0].text.strip()]}
            row_dict['symbol'] = (row_dict['variety'] + x[1].text.strip())
            for (i, field) in enumerate(listed_columns):
                field_content = x[(i + 2)].text.strip()
                if ('-' in field_content):
                    row_dict[field] = 0
                elif (field in ['volume', 'open_interest']):
                    row_dict[field] = int(field_content.replace(',', ''))
                else:
                    row_dict[field] = float(field_content.replace(',', ''))
            dict_data.append(row_dict)
        elif (len(x) == 16):
            m = ct.FUTURE_SYMBOL_PATTERN.match(x[1].text.strip())
            if (not m):
                continue
            row_dict = {'symbol': x[1].text.strip(), 'variety': m.group(1).upper(), 'contract_id': m.group(0)}
            for (i, field) in enumerate(listed_columns):
                field_content = x[(i + 2)].text.strip()
                if ('-' in field_content):
                    row_dict[field] = 0
                elif (field in ['volume', 'open_interest']):
                    row_dict[field] = int(field_content.replace(',', ''))
                else:
                    row_dict[field] = float(field_content.replace(',', ''))
            dict_data.append(row_dict)
        elif (len(x) == 2):
            implied_data.append({'contract_id': x[0].text.strip(), 'implied_volatility': float(x[1].text.strip())})
    df = pd.DataFrame(dict_data)
    df['date'] = day.strftime('%Y%m%d')
    if (type == 'future'):
        return df[output_columns]
    else:
        return pd.merge(df, pd.DataFrame(implied_data), on='contract_id', how='left', indicator=False)[output_columns]
