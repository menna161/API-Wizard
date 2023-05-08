from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_mlb_team_score(query_team):
    " put in the long for name of the team of interest:\n\t\ti.e. 'Toronto Blue Jays', 'New York Yankees' "
    baseball_reference = 'http://www.baseball-reference.com/'
    mlb_dat = urlopen(baseball_reference)
    mlb_scores = BeautifulSoup(mlb_dat, 'lxml')
    game_section = mlb_scores.find(id='scores')
    yesterday_games = game_section.findAll('', {'class', 'teams'})
    for game in yesterday_games:
        winner = game.find('', {'class': 'winner'})
        w_team = winner.td.get_text()
        loser = game.find('', {'class': 'loser'})
        l_team = loser.td.get_text()
        if ((w_team != query_team) and (l_team != query_team)):
            continue
        else:
            w_score = winner.find('', {'class': 'right'}).get_text()
            l_score = loser.find('', {'class': 'right'}).get_text()
            return {w_team: w_score, l_team: l_score}
    return 'did not play yesterday'
