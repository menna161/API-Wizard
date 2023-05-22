import json
from collections import namedtuple
from typing import Generator
import requests
from bs4 import BeautifulSoup


@property
def total_pages(self) -> int:
    if self.__data_ismodified:
        response = requests.post('https://context.reverso.net/bst-query-service', headers=HEADERS, data=json.dumps(self.__data))
        total_pages = response.json()['npages']
        if (not isinstance(total_pages, int)):
            try:
                total_pages = int(total_pages)
            except ValueError:
                raise ValueError('"npages" in the response cannot be interpreted as an integer')
        if (total_pages < 0):
            raise ValueError('"npages" in the response is a negative number')
        self.__total_pages = total_pages
        self.__data_ismodified = False
    return self.__total_pages
