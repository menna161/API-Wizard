import json
from collections import namedtuple
from typing import Generator
import requests
from bs4 import BeautifulSoup


@staticmethod
def __get_supported_langs() -> dict:
    supported_langs = {}
    response = requests.get('https://context.reverso.net/translation/', headers=HEADERS)
    soup = BeautifulSoup(response.content, features='lxml')
    src_selector = soup.find('div', id='src-selector')
    trg_selector = soup.find('div', id='trg-selector')
    for (selector, attribute) in ((src_selector, 'source_lang'), (trg_selector, 'target_lang')):
        dd_spans = selector.find(class_='drop-down').find_all('span')
        langs = [span.get('data-value') for span in dd_spans]
        langs = [lang for lang in langs if (isinstance(lang, str) and (len(lang) == 2))]
        supported_langs[attribute] = tuple(langs)
    return supported_langs
