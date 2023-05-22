from urllib.request import Request, urlopen
import urllib.parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
from .errors import *


def parse_citation(self, single_citation):
    'Parses patent citation, returning results as a dictionary\n\n\n        Returns (variables returned in dictionary, following are key names):  \n            - patent_number (str)  : patent number\n            - priority_date (str)  : priority date of patent\n            - pub_date      (str)  : publication date of patent\n\n        Inputs:\n            - single_citation (str) : html string from citation section in google patent html\n\n        '
    try:
        patent_number = single_citation.find('span', itemprop='publicationNumber').get_text()
    except:
        patent_number = ''
    try:
        priority_date = single_citation.find('td', itemprop='priorityDate').get_text()
    except:
        priority_date = ''
    try:
        pub_date = single_citation.find('td', itemprop='publicationDate').get_text()
    except:
        pub_date
    return {'patent_number': patent_number, 'priority_date': priority_date, 'pub_date': pub_date}
