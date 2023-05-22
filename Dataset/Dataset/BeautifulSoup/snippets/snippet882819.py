import click
from urllib.parse import parse_qsl, urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def parse_example(url: str):
    ' extract the example sentences '
    html = requests.get(url).text
    bs = BeautifulSoup(html, 'html.parser')
    list_ = bs.findAll('li')
    sentences = []
    for l in list_:
        eng_phrase = l.find('span', attrs={'txt_example'}).text.split('\n')[0]
        mean_phrase = l.find('span', attrs={'mean_example'}).text
        phrase_set = f'''{eng_phrase}
  -> {mean_phrase}

'''
        sentences.append(phrase_set)
    return ''.join(sentences)
