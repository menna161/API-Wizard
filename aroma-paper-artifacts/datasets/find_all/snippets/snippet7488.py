import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def is_valid(self):
    ingredient_list = self.soup.find_all('li', {'class': 'IngredientLine'})
    return bool(ingredient_list)
