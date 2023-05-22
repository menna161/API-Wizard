from __future__ import absolute_import, division, print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer
import requests
from termcolor import colored


def get_post_summaries(query):
    '\n    A generator that queries Stack Overflow and yields a ResultSet\n    of post summaries.\n\n    Parameter {str} query: the string to query Stack Overflow with.\n    Yields {bs4.element.ResultSet}: ResultSet of post summaries.\n    '
    page = 1
    while True:
        query_url = build_query_url(query, page)
        query_soup = query_stack_overflow(query_url)
        if (not query_soup):
            break
        post_summaries = query_soup.find_all(attrs={'class': 'question-summary'})
        if (not post_summaries):
            break
        (yield post_summaries)
        page += 1
