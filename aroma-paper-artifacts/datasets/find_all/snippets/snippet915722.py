import os
import requests
from bs4 import BeautifulSoup
import tqdm
import json
import difflib
import random


def download_thai_address():
    print('Downloading the address information of Thailand ...')
    url = 'https://en.wikipedia.org/wiki/List_of_tambon_in_Thailand'
    data = requests.get(url).text
    data = BeautifulSoup(data, 'html.parser')
    urls = data.find_all(name='ul')[0]
    hrefs = urls.find_all(name='li')
    res = {}
    th_en = {}
    for h in tqdm.tqdm(hrefs):
        href = ('https://en.wikipedia.org/' + h.find(name='a')['href'])
        data = requests.get(href).text
        data = BeautifulSoup(data, 'html.parser')
        table = data.find_all(name='table', attrs={'class': 'wikitable sortable'})
        details = table[0].find_all(name='tr')[1:]
        for detail in details:
            temp = detail.find_all(name='td')
            sub_district = temp[1].text
            district = temp[3].text
            province = temp[5].text
            th_en[sub_district] = temp[0].text
            th_en[district] = temp[2].text
            th_en[province] = temp[4].text
            if (province in res.keys()):
                if (district in res[province].keys()):
                    if (sub_district not in res[province][district]):
                        res[province][district].append(sub_district)
                else:
                    res[province][district] = [sub_district]
            else:
                res[province] = {district: [sub_district]}
    for p in res.keys():
        for d in res[p].keys():
            res[p][d] = list(set(res[p][d]))
    json.dump(res, open('th_provinces_districts_sub_districts.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(th_en, open('th_en_db.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print('Finish the downloading!')
