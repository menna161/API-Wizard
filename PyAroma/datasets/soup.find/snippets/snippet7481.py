import requests
from bs4 import BeautifulSoup
from core.utils import translate_many


def get_recipe_title(self):
    title = self.soup.find('h1', {'class': 'przepis page-header'})
    return title.get_text().strip()
