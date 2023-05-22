import base64
import re
from datetime import datetime
from urllib.parse import quote, urlparse
import cfscrape
import requests
from bs4 import BeautifulSoup
from psaripper.PSAMedia import PSAMedia


def decrypt_url(url, scraper: cfscrape.CloudflareScraper):
    urlr = scraper.get(url)
    soup = BeautifulSoup(urlr.content, 'html.parser')
    ouo_url = soup.find('form')['action']
    furl = bypass_ouo(ouo_url)
    return get_urls(furl)
