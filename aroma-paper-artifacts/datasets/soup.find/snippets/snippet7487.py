import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def get_count_of_servings(self):
    servings = self.soup.find('div', {'class': 'servings'})
    if servings:
        return int(servings.find('input')['value'])
    return 1
