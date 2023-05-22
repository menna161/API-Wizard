import json
import requests
import random
from lxml import html
from selenium import webdriver


def fetch_proxies() -> list:
    'fetch list of proxies from url'
    url = 'https://www.sslproxies.org/'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    elements = tree.xpath('//*[@id="proxylisttable"]/tbody')[0]
    proxies = []
    keys = ['ip', 'port', 'code', 'country', 'anonymity', 'google', 'https', 'last_checked']
    for row in elements.getchildren():
        values = [col.text for col in row.getchildren()]
        proxies.append(dict(zip(keys, values)))
    return proxies
