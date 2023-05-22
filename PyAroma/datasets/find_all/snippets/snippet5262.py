import enum
import json
import logging
import os
import re
import time
from typing import Generator, BinaryIO, Iterable
import requests
from bs4 import BeautifulSoup as Soup
from bs4 import element
from saucenao import http
from saucenao.exceptions import *


@staticmethod
def parse_results_html_to_json(html: str) -> str:
    'Parse the results and sort them descending by similarity\n\n        :type html: str\n        :return:\n        '
    soup = Soup(html, 'html.parser')
    results = {'header': {}, 'results': []}
    for res in soup.find_all('td', attrs={'class': 'resulttablecontent'}):
        title_tag = res.find_next('div', attrs={'class': 'resulttitle'})
        if title_tag:
            title = title_tag.text
        else:
            title = ''
        similarity = res.find_next('div', attrs={'class': 'resultsimilarityinfo'}).text.replace('%', '')
        alternate_links = [a_tag['href'] for a_tag in res.find_next('div', attrs={'class': 'resultmiscinfo'}).find_all('a', href=True)]
        content_column = []
        content_column_tags = res.find_all('div', attrs={'class': 'resultcontentcolumn'})
        for content_column_tag in content_column_tags:
            for br in content_column_tag.find_all('br'):
                br.replace_with('\n')
            content_column.append(content_column_tag.text)
        result = {'header': {'similarity': similarity}, 'data': {'title': title, 'content': content_column, 'ext_urls': alternate_links}}
        results['results'].append(result)
    return json.dumps(results)
