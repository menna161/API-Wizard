from bs4 import BeautifulSoup
from DbManager import DatabaseManager
import json
import re
import time
from selenium import webdriver
from SoccerMatch import SoccerMatch


def get_odds(self, tag):
    '\n        Extract the betting odds for a match from an HTML tag for a soccer\n        match row.\n\n        Args:\n            tag (obj): HTML tag object from BeautifulSoup.\n\n        Returns:\n            (list of str) Extracted match odds.\n        '
    odds_cells = tag.find_all(class_='odds-nowrp')
    odds = []
    for cell in odds_cells:
        odds.append(cell.text)
    return odds
