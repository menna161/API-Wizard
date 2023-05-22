import os
import io
import re
import time
import json
import pathlib
import argparse
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def recipeToJSON(browser, recipeID):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    recipe = {}
    recipe['id'] = recipeID
    recipe['language'] = soup.select_one('html').attrs['lang']
    recipe['title'] = soup.select_one('.recipe-card__title').text
    recipe['rating_count'] = re.sub('\\D', '', soup.select_one('.core-rating__label').text, flags=re.IGNORECASE)
    recipe['rating_score'] = soup.select_one('.core-rating__counter').text
    recipe['tm-versions'] = [v.text.replace('\n', '').strip().lower() for v in soup.select('.recipe-card__tm-version core-badge')]
    recipe.update({l.text: l.next_sibling.strip() for l in soup.select('core-feature-icons label span')})
    recipe['ingredients'] = [re.sub(' +', ' ', li.text).replace('\n', '').strip() for li in soup.select('#ingredients li')]
    recipe['nutritions'] = {}
    for item in list(zip(soup.select('.nutritions dl')[0].find_all('dt'), soup.select('.nutritions dl')[0].find_all('dd'))):
        (dt, dl) = item
        recipe['nutritions'].update({dt.string.replace('\n', '').strip().lower(): re.sub('\\s{2,}', ' ', dl.string.replace('\n', '').strip().lower())})
    recipe['steps'] = [re.sub(' +', ' ', li.text).replace('\n', '').strip() for li in soup.select('#preparation-steps li')]
    recipe['tags'] = [a.text.replace('#', '').replace('\n', '').strip().lower() for a in soup.select('.core-tags-wrapper__tags-container a')]
    return recipe
