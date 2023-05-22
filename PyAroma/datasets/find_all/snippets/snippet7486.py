import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def get_list_of_ingredients(self):
    ingredient_list = self.soup.find_all('li', {'class': 'IngredientLine'})
    return [ing.get_text().strip() for ing in ingredient_list]
