from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def GetCategory2Type2(self, resp):
    '获取第二种类型的小类链接'
    category2Type2Urls = {}
    soup = BeautifulSoup(resp.text, 'html.parser')
    dict_td_lists = soup.find_all('div', class_='cate_no_child no_select')
    for dict_td_list in dict_td_lists:
        dict_td_url = ('https://pinyin.sogou.com' + dict_td_list.a['href'])
        category2Type2Urls[dict_td_list.get_text().replace('\n', '')] = dict_td_url
    dict_td_lists = soup.find_all('div', class_='cate_has_child no_select')
    for dict_td_list in dict_td_lists:
        dict_td_url = ('https://pinyin.sogou.com' + dict_td_list.a['href'])
        category2Type2Urls[dict_td_list.get_text().replace('\n', '')] = dict_td_url
    return category2Type2Urls
