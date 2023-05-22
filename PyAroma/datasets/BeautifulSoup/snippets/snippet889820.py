import re
from bs4 import BeautifulSoup, Comment, Tag, NavigableString
import codecs


def read_html(file):
    with codecs.open(file, 'r', encoding='UTF-8') as f:
        text = f.read()
    return BeautifulSoup(text, 'html.parser')
