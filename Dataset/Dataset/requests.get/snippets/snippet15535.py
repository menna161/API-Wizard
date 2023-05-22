import re
import os
import sys
import random
import hashlib
import asyncio
from datetime import datetime
from typing import Generator, List
import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from lxml import html


def get_proxies(anonymity: str='elite proxy') -> List[str]:
    ' get list of free proxies '
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    parser = html.fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if (i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath(f'.//td[5][contains(text(),"{anonymity}")]')):
            proxy = ':'.join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
