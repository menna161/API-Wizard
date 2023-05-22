from bs4 import BeautifulSoup
from dexy.filter import DexyFilter
from dexy.utils import chdir
import base64
import inflection
import mimetypes
import re
import urllib


def inline_images(self, soup):
    for tag in soup.find_all('img'):
        path = tag.get('src')
        f = urllib.urlopen(path)
        data = f.read()
        f.close()
        (mime, _) = mimetypes.guess_type(path)
        data64 = base64.encodestring(data)
        dataURI = ('data:%s;base64,%s' % (mime, data64))
        tag['src'] = dataURI
