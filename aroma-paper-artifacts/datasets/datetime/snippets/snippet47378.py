from bs4 import BeautifulSoup
from DbManager import DatabaseManager
import json
import re
import time
from selenium import webdriver
from SoccerMatch import SoccerMatch


def scrape_url(self, url):
    '\n        Scrape the data for every match on a given URL and insert each into the\n        database.\n\n        Args:\n            url (str): URL to scrape data from.\n\n        Returns:\n            Whether data existed for that season.\n        '
    self.browser.get(url)
    delay = 5
    time.sleep(delay)
    tournament_tbl = self.browser.find_element_by_id('tournamentTable')
    tournament_tbl_html = tournament_tbl.get_attribute('innerHTML')
    tournament_tbl_soup = BeautifulSoup(tournament_tbl_html, 'html.parser')
    try:
        significant_rows = tournament_tbl_soup(self.is_soccer_match_or_date)
    except:
        return False
    current_date_str = None
    for row in significant_rows:
        if (self.is_date(row) is True):
            current_date_str = self.get_date(row)
        elif (self.is_date_string_supported(current_date_str) == False):
            continue
        else:
            this_match = SoccerMatch()
            game_datetime_str = ((current_date_str + ' ') + self.get_time(row))
            this_match.set_start(game_datetime_str)
            participants = self.get_participants(row)
            this_match.set_teams(participants)
            scores = self.get_scores(row)
            this_match.set_outcome_from_scores(scores)
            odds = self.get_odds(row)
            this_match.set_odds(odds)
            self.db_manager.add_soccer_match(self.league, url, this_match)
    return True
