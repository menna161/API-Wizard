import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def get_count_of_servings(self):
    servings_div = self.soup.find('div', 'field field-name-field-ilosc-porcji field-type-text field-label-hidden')
    if servings_div:
        for w in servings_div.get_text().strip().split(' '):
            if w.isnumeric():
                return int(w)
    return 1
