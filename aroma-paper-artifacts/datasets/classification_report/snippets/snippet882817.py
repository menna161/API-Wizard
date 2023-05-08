import click
from urllib.parse import parse_qsl, urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def parse(html: str):
    bs = BeautifulSoup(html, 'html.parser')
    content = bs.findAll('meta', attrs={'property': 'og:description'})[0].get('content')
    if (not content):
        return ('No results found.', '')
    try:
        redir_url = bs.findAll('meta', attrs={'http-equiv': 'Refresh'})[0].get('content').split('URL=')[1]
    except IndexError:
        redir_url = bs.findAll('a', attrs={'txt_cleansch'})[0].attrs['href']
    dic_query = urlparse(redir_url).query
    wordid = dict(parse_qsl(dic_query))['wordid']
    return (content, wordid)
