from dexy.data import Generic
from bs4 import BeautifulSoup


def soup(self):
    '\n        Returns a BeautifulSoup object initialized with contents.\n        '
    if (not hasattr(self, '_soup')):
        self._soup = BeautifulSoup(self.data())
    return self._soup
