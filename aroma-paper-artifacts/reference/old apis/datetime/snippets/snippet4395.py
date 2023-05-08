import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from aao.spiders.spider import Spider
from aao.spiders import sports


def _parse_teams(self, row):
    (teams, msg) = ([], '')
    try:
        datetime.datetime.strptime(row[1], '%I:%M %p')
        if ('X' in row):
            index = row.index('X')
            teams_list = row[(index - 2)::4]
        else:
            teams_list = [row[2], row[4]]
    except ValueError:
        if ('+' in row[1]):
            row.pop(1)
        teams_list = row[1].split(' - ')
        teams_list[1] = ' '.join(teams_list[1].split(' ')[:(- 2)])
    for i in teams_list:
        team = self.teams(self.country, self.league, full=True).get(i)
        teams.append(team)
        if (not team):
            msg = (f'{i} not in bookmaker teams table. ' + msg)
    if (None in teams):
        raise KeyError((msg + 'Tables need an upgrade, notify the devs.'))
    return teams
