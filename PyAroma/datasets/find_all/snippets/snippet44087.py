from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def GetCategoryOne(self, resp):
    '获取大类链接'
    categoryOneUrls = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    dict_nav = soup.find('div', id='dict_nav_list')
    dict_nav_lists = dict_nav.find_all('a')
    for dict_nav_list in dict_nav_lists:
        dict_nav_url = ('https://pinyin.sogou.com' + dict_nav_list['href'])
        categoryOneUrls.append(dict_nav_url)
    return categoryOneUrls
