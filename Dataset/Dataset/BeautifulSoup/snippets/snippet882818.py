import click
from urllib.parse import parse_qsl, urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def parse_detail(html: str, wordid: str, category: str):
    ' parse once more to get the detailed view '
    bs = BeautifulSoup(html, 'html.parser')
    id_set = {'antonym': 'OPPOSITE_WORD', 'synonym': 'SIMILAR_WORD'}
    if (category not in id_set.keys()):
        pass
    else:
        words = bs.find(id=id_set[category])
        if (not words):
            return 'No results found.'
        tags = words.findAll('li')
        result = [f"{tag.find('a').text}: {tag.find('span').text}" for tag in tags]
        return '\n'.join(result)
