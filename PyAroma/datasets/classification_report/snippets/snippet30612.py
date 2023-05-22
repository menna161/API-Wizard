from bs4 import BeautifulSoup
from dexy.filter import DexyFilter
from dexy.utils import chdir
import base64
import inflection
import mimetypes
import re
import urllib


def process_text(self, input_text):
    soup = BeautifulSoup(input_text)
    for js in self.setting('scripts'):
        js_tag = soup.new_tag('script', type='text/javascript', src=js)
        soup.head.append(js_tag)
    for css in self.setting('stylesheets'):
        css_tag = soup.new_tag('link', rel='stylesheet', type='text/css', href=css)
        soup.head.append(css_tag)
    return str(soup)
