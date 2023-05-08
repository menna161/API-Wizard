import os
import math
import random
import gzip
import requests
from bs4 import BeautifulSoup
from seodeploy.modules.contentking import SEOTestingModule
from seodeploy.lib.logging import get_logger
from seodeploy.lib.helpers import url_to_path


def read_sitemap_urls(sitemap_url, limit=None):
    ' Grabs recursive URLs from a sitemap or sitemap index.\n\n    Parameters\n    ----------\n    sitemap_url: str\n        URL of the sitemap (XML).\n    limit: int\n        Restict to this many results.\n\n    Returns\n    -------\n    list\n        All found URLs\n\n    '
    all_urls = []
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Accept-Encoding': 'gzip'}
    try:
        response = requests.get(sitemap_url, headers=headers)
        if (response.headers['Content-Type'].lower() == 'application/x-gzip'):
            xml = gzip.decompress(response.content)
        else:
            xml = response.content
        soup = BeautifulSoup(xml, 'lxml')
        urls = [url.get_text().lower() for url in soup.find_all('loc')]
        while urls:
            url = urls.pop(0)
            if ('.xml' in url[(- 8):]):
                urls.extend(read_sitemap_urls(url))
                continue
            all_urls.append(url)
            if (limit and (len(all_urls) >= limit)):
                break
    except Exception as e:
        _LOG.error('Read Sitemap Error: ', str(e))
    return all_urls
