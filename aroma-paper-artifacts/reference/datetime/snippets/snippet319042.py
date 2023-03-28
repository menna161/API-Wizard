import os
from conf import conf
import numpy as np
import datetime
import h5py
import tqdm
from sgfsave import save_game_sgf
from play import index2coord, make_play, game_init, show_board, get_winner
from engine import ModelEngine
from random import random


def self_play(model, n_games, mcts_simulations):
    desc = ('Self play %s' % model.name)
    games = tqdm.tqdm(range(n_games), desc=desc)
    games_data = []
    current_resign = None
    min_values = []
    for game in games:
        if (random() > RESIGNATION_PERCENT):
            resign = current_resign
        else:
            resign = None
        start = datetime.datetime.now()
        game_data = play_game(model, model, mcts_simulations, conf['STOP_EXPLORATION'], self_play=True, resign_model1=resign, resign_model2=resign)
        stop = datetime.datetime.now()
        if (resign == None):
            winner = game_data['winner']
            if (winner == 1):
                min_value = min([move['value'] for move in game_data['moves'][::2]])
            else:
                min_value = min([move['value'] for move in game_data['moves'][1::2]])
            min_values.append(min_value)
            l = len(min_values)
            resignation_index = int((RESIGNATION_ALLOWED_ERROR * l))
            if (resignation_index > 0):
                current_resign = min_values[resignation_index]
        moves = len(game_data['moves'])
        speed = (((stop - start).seconds / moves) if moves else 0.0)
        games.set_description((desc + (' %s moves %.2fs/move ' % (moves, speed))))
        save_game_data(model.name, game_data)
        games_data.append(game_data)
    return games_data
