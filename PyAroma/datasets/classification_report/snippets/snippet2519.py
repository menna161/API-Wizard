from __future__ import absolute_import, division, print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer
import requests
from termcolor import colored


def post_soup(post_summary):
    '\n    Given a post summary, query Stack Overflow, and return the\n    BeautifulSoup of the post, if it has an accepted answer.\n\n    Parameter {bs4.Tag} post_summary: the bs4.Tag post summary.\n    Parameter {bs4.BeautifulSoup}: the BeautifulSoup of the post,\n    if it has an accepted answer; otherwise, None.\n    '
    if has_accepted_answer(post_summary):
        post_url = get_post_url(post_summary)
        try:
            response = requests.get((BASE_URL + post_url))
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        return BeautifulSoup(response.text, 'lxml')
    return None
