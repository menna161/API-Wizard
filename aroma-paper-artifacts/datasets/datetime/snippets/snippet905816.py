import base64
import re
from datetime import datetime
from urllib.parse import quote, urlparse
import cfscrape
import requests
from bs4 import BeautifulSoup
from psaripper.PSAMedia import PSAMedia


def create_scraper(**kwargs):
    today = datetime.utcnow().strftime('%Y%m%d')
    today_2 = base64.b64encode(datetime.utcnow().strftime('%d%m%y').encode()).decode()
    visit_cnt = 6
    visit_cnt = quote(base64.b64encode(str(visit_cnt).encode()).decode())
    headers = {'Cookie': f'clks={today}; ez4s={(int(today) + 1)}; LstVstD={today_2}; shrnkio={today}; try2={today}; VstCnt={visit_cnt};', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    headers.update(kwargs)
    scraper = cfscrape.create_scraper(headers=headers)
    return scraper
