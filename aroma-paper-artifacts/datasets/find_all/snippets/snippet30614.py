from bs4 import BeautifulSoup
from dexy.filter import DexyFilter
from dexy.utils import chdir
import base64
import inflection
import mimetypes
import re
import urllib


def inline_styles(self, soup):
    for tag in soup.find_all('link'):
        path = tag.get('href')
        f = urllib.urlopen(path)
        data = f.read()
        f.close()
        style = soup.new_tag('style')
        style.string = data
        tag.replace_with(style)
