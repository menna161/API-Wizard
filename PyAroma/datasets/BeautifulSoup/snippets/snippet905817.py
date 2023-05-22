import base64
import re
from datetime import datetime
from urllib.parse import quote, urlparse
import cfscrape
import requests
from bs4 import BeautifulSoup
from psaripper.PSAMedia import PSAMedia


def get_urls(url):
    scraper = create_scraper(referer=url)
    try:
        res = scraper.get(url)
        c = res.content
        soup = BeautifulSoup(c, 'lxml')
        entry = soup.find_all('div', 'entry-content')[0]
        links = entry.find_all('a')
        return [x.get('href') for x in links]
    except Exception:
        return [url]
