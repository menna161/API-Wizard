from bs4 import BeautifulSoup
from urllib.parse import unquote
import requests
import re
import os


def GetDownloadList(self, resp):
    '获取下载链接'
    downloadUrls = {}
    pattern = re.compile('name=(.*)')
    soup = BeautifulSoup(resp.text, 'html.parser')
    dict_dl_lists = soup.find_all('div', class_='dict_dl_btn')
    for dict_dl_list in dict_dl_lists:
        dict_dl_url = dict_dl_list.a['href']
        dict_name = pattern.findall(dict_dl_url)[0]
        dict_ch_name = unquote(dict_name, 'utf-8').replace('/', '-').replace(',', '-').replace('|', '-').replace('\\', '-').replace("'", '-')
        downloadUrls[dict_ch_name] = dict_dl_url
    return downloadUrls
