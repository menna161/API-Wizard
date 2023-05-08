import re
import os
import json
import execjs
import pickle
import platform
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_seat_dynamic_info(cookies, project_id, item_id, perform_id):
    ' 获取 standId, 用于获取所有座位信息 '
    headers = {'authority': 'mtop.damai.cn', 'accept': 'application/json', 'accept-language': 'zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7', 'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://seatsvc.damai.cn', 'referer': 'https://seatsvc.damai.cn/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    h5_token = cookies.get('_m_h5_tk').split('_')[0]
    time_stamp = int((datetime.now().timestamp() * 1000))
    api_param = json.dumps({'projectId': project_id, 'performanceId': perform_id, 'itemId': item_id, 'hasPromotion': 'true', 'dmChannel': 'pc@damai_pc'}).replace(' ', '')
    sign_code = get_sign_code(h5_token, time_stamp, api_param)
    params = {'jsv': '2.6.0', 'appKey': '12574478', 't': time_stamp, 'sign': sign_code, 'type': 'originaljson', 'dataType': 'json', 'v': '1.0', 'H5Request': 'true', 'AntiCreep': 'true', 'AntiFlood': 'true', 'api': 'mtop.damai.wireless.seat.dynamicinfo', 'data': api_param}
    response = requests.get('https://mtop.damai.cn/h5/mtop.damai.wireless.seat.dynamicinfo/1.0/', params=params, cookies=cookies, headers=headers)
    if (response.status_code == 200):
        result = json.loads(response.text).get('data')
        stand_id = result.get('standColorList')[0].get('standId')
        seat_price_list = result.get('priceList')
        return (stand_id, seat_price_list)
