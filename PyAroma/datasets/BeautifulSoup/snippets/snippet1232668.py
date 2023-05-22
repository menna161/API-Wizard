import re
import argparse
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
from collections import Counter, defaultdict
from math import log10
from bs4 import BeautifulSoup
import numpy as np


def parse(html, url, bases):
    '\n    Takes an html string and a url as arguments.\n\n    Returns a tuple (url, content, links) parsed from the html.\n    '
    soup = BeautifulSoup(html, 'lxml')
    content = soup.body.get_text().strip()
    links = [urljoin(url, l.get('href')) for l in soup.findAll('a')]
    links = [l for l in links if (urlparse(l).netloc in bases)]
    return (url, content, links)
