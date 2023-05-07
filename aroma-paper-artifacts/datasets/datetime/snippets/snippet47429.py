from .models import Game
from .models import Season
from pyquery import PyQuery as pyquery
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import logging
import os
import re
import time


def populate_games_into_season(self, season):
    '\n        Params:\n            season (Season) with urls but not games populated, to modify\n        '
    for url in season.urls:
        self.go_to_link(url)
        html_source = self.get_html_source()
        html_querying = pyquery(html_source)
        no_data_div = html_querying.find('div.message-info > ul > li > div.cms')
        if ((no_data_div != None) and (no_data_div.text() == 'No data available')):
            logger.warning('Found "No data available", skipping %s', url)
            continue
        retrieval_time_for_reference = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        tournament_table = html_querying.find('div#tournamentTable > table#tournamentTable')
        table_rows = tournament_table.find('tbody > tr')
        num_table_rows = len(table_rows)
        for i in range(0, num_table_rows):
            try:
                time_cell = tournament_table.find('tbody > tr').eq(i).find('td.table-time')
                if (0 == len(str(time_cell).strip())):
                    continue
                game = Game()
                time_cell = time_cell[0]
                for (key, value) in time_cell.attrib.items():
                    if (key == 'class'):
                        time_cell_classes = value.split(' ')
                        for time_cell_class in time_cell_classes:
                            if ((0 == len(time_cell_class)) or (time_cell_class[0] != 't')):
                                continue
                            if ((time_cell_class[1] == '0') or (time_cell_class[1] == '1') or (time_cell_class[2] == '2')):
                                unix_time = int(time_cell_class.split('-')[0].replace('t', ''))
                                game.game_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_time))
                                break
                        break
                if (0 == len(game.game_datetime)):
                    continue
                game.retrieval_datetime = retrieval_time_for_reference
                game.retrieval_url = url
                game.num_possible_outcomes = season.possible_outcomes
                number_of_outcomes = season.possible_outcomes
                participants_link = tournament_table.find('tbody > tr').eq(i).find('td.table-participant > a')
                participants = participants_link.text().split(' - ')
                game.team_home = participants[0]
                game.team_away = participants[1]
                game.game_url = (self.base_url + participants_link[0].attrib['href'])
                overall_score_cell = tournament_table.find('tbody > tr').eq(i).find('td.table-score')
                overall_score_string = overall_score_cell.text()
                overall_score_string = overall_score_string.split()[0]
                if (':' in overall_score_string):
                    game.score_home = int(overall_score_string.split(':')[0])
                    game.score_away = int(overall_score_string.split(':')[1])
                elif ('-' in overall_score_string):
                    game.score_home = int(overall_score_string.split('-')[0])
                    game.score_away = int(overall_score_string.split('-')[1])
                else:
                    logger.warning('Could not split score string - delimiter unknown')
                    raise RuntimeError('Could not split score string - delimiter unknown')
                if (game.score_home > game.score_away):
                    game.outcome = 'HOME'
                elif (game.score_home < game.score_away):
                    game.outcome = 'AWAY'
                else:
                    game.outcome = 'DRAW'
                individual_odds_links = tournament_table.find('tbody > tr').eq(i).find('td.odds-nowrp > a')
                if (len(individual_odds_links) < 2):
                    continue
                elif ((number_of_outcomes != 2) and (number_of_outcomes != 3)):
                    raise RuntimeError(('Unsupported number of outcomes specified - ' + str(number_of_outcomes)))
                for (x, individual_odds_link) in enumerate(individual_odds_links):
                    if (2 == number_of_outcomes):
                        if (x == 0):
                            game.odds_home = individual_odds_link.text
                        else:
                            game.odds_away = individual_odds_link.text
                    elif (3 == number_of_outcomes):
                        if (x == 0):
                            game.odds_home = individual_odds_link.text
                        elif (x == 1):
                            game.odds_draw = individual_odds_link.text
                        else:
                            game.odds_away = individual_odds_link.text
                if (number_of_outcomes == 2):
                    game.odds_draw = None
                season.add_game(game)
            except Exception as e:
                logger.warning('Skipping row, encountered exception - data format not as expected')
                continue
