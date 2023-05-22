import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def is_valid(self):
    ingredients_div = self.soup.find('div', 'field field-name-field-skladniki field-type-text-long field-label-hidden')
    return bool(ingredients_div)
