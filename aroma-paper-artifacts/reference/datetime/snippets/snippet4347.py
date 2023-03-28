import datetime
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from aao.spiders.spider import Spider
from aao.spiders import sports


def _parse_event(self, row):
    datetime = self._parse_datetime(row)
    (home_team, away_team) = self._parse_teams(row)
    event = {'datetime': datetime, 'country': self.country, 'league': self.league, 'home_team': home_team, 'away_team': away_team}
    return event
