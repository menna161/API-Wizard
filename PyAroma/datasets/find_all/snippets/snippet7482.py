import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def get_list_of_ingredients(self):
    ingredients_div = self.soup.find('div', 'field field-name-field-skladniki field-type-text-long field-label-hidden')
    ingredient_list = ingredients_div.find_all('li')
    return [ing.get_text().strip() for ing in ingredient_list]
