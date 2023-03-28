import time
import calendar
import datetime
import re
import os
import json
import logging
import sys
import requests
from bs4 import BeautifulSoup
from analysisDXY import *


def main():
    DX_html = requests.get(URL_DX)
    DX_html.encoding = 'utf-8'
    DX_html_soup = BeautifulSoup(DX_html.content, 'lxml')
    DX_script_listByCountry = str(DX_html_soup.find('script', attrs={'id': 'getListByCountryTypeService1'}))
    DX_content_listByCountry = re.search('\\[(.*?)\\]', DX_script_listByCountry).group()
    utc_now = time.gmtime()
    DX_utc_str = ((str((((utc_now[0] * (100 ** 2)) + (utc_now[1] * 100)) + utc_now[2])) + '_') + str((((utc_now[3] * (100 ** 2)) + (utc_now[4] * 100)) + utc_now[5])))
    if (utc_now[3] < 10):
        DX_utc_str = ((DX_utc_str.split('_')[0] + '_0') + DX_utc_str.split('_')[1])
    with open((((os.getcwd() + '\\data\\DXYjson\\DXY_') + DX_utc_str) + '.json'), 'w', encoding='utf-8') as f:
        f.write(DX_content_listByCountry.replace(',', ',\n'))
        logger.info('[done] file - {} saved.'.format((('DXY_' + DX_utc_str) + '.json')))
    f.close()
    with open((os.getcwd() + '\\arc\\DXY_bycity_compilation.json'), 'a', encoding='utf-8') as f:
        f.write(DX_content_listByCountry)
        f.write('\n')
        logger.info('[update] file - {} updated - {}'.format('DXY_bycity_compilation.json', str(datetime.datetime.now())))
    f.close()
    with open((os.getcwd() + '\\arc\\DXY_full_compilation.json'), 'a', encoding='utf-8') as f:
        f.write('\n{} START - {} {}\n'.format(('=' * 10), DX_utc_str, ('=' * 10)))
        f.write(str(DX_html_soup))
        f.write('\n{} END - {} {}\n'.format(('=' * 10), DX_utc_str, ('=' * 10)))
        logger.info('[update] file - {} updated - {}'.format('DXY_full_compilation.json', str(datetime.datetime.now())))
    f.close()
    DX_content_dict = json.loads(DX_content_listByCountry)
    return (DX_content_listByCountry, DX_content_dict)
