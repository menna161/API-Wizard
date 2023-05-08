from __future__ import absolute_import, division, print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer
import requests
from termcolor import colored


def query_stack_overflow(url):
    '\n    Given a url, this function returns the BeautifulSoup of the\n    request.\n\n    Parameter {str} url: the url to request.\n    Returns {bs4.BeautifulSoup}: the BeautifulSoup of the request.\n    '
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
    return BeautifulSoup(response.text, 'lxml')
