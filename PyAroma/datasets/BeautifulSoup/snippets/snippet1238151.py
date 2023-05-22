from urllib.request import Request, urlopen
import urllib.parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
from .errors import *


def request_single_patent(self, patent, url=False):
    'Calls request function to retreive google patent data and parses returned html using BeautifulSoup\n\n\n        Returns: \n            - Status of scrape   <- String\n            - Html of patent     <- BS4 object\n\n        Inputs:\n            - patent (str)  : if    url == False then patent is patent number\n                              elif  url == True  then patent is google patent url\n            - url    (bool) : determines whether patent is treated as patent number \n                                or google patent url\n\n        '
    try:
        if (not url):
            url = 'https://patents.google.com/patent/{0}'.format(patent)
        else:
            url = patent
        print(url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, features='lxml')
        return ('Success', soup, url)
    except HTTPError as e:
        print('Patent: {0}, Error Status Code : {1}'.format(patent, e.code))
        return (e.code, '', url)
