from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def GetPage(self, resp):
    '获取页码'
    soup = BeautifulSoup(resp.text, 'html.parser')
    dict_div_lists = soup.find('div', id='dict_page_list')
    dict_td_lists = dict_div_lists.find_all('a')
    page = dict_td_lists[(- 2)].string
    return int(page)
