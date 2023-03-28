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


def play_game(model1, model2, mcts_simulations, stop_exploration, self_play=False, num_moves=None, resign_model1=None, resign_model2=None):
    (board, player) = game_init()
    moves = []
    engine1 = ModelEngine(model1, mcts_simulations, resign=resign_model1, temperature=1, board=np.copy(board), add_noise=self_play)
    engine2 = ModelEngine(model2, mcts_simulations, resign=resign_model2, temperature=1, board=np.copy(board), add_noise=self_play)
    if self_play:
        engine2.tree = engine1.tree
    last_value = None
    value = None
    skipped_last = False
    start = datetime.datetime.now()
    end_reason = 'PLAYED ALL MOVES'
    if (num_moves is None):
        num_moves = ((SIZE * SIZE) * 2)
    for move_n in range(num_moves):
        last_value = value
        if (move_n == stop_exploration):
            engine1.set_temperature(0)
            engine2.set_temperature(0)
        if ((move_n % 2) == 0):
            (x, y, policy_target, value, _, _, policy) = engine1.genmove('B')
            if (y == (SIZE + 1)):
                end_reason = 'RESIGN'
                break
            engine2.play('B', x, y, update_tree=(not self_play))
        else:
            (x, y, policy_target, value, _, _, policy) = engine2.genmove('W')
            if (y == (SIZE + 1)):
                end_reason = 'RESIGN'
                break
            engine1.play('B', x, y, update_tree=(not self_play))
        move_data = {'board': np.copy(board), 'policy': policy_target, 'policy_variation': np.linalg.norm((policy_target - policy)), 'value': value, 'move': (x, y), 'move_n': move_n, 'player': player}
        moves.append(move_data)
        if (skipped_last and (y == SIZE)):
            end_reason = 'BOTH_PASSED'
            break
        skipped_last = (y == SIZE)
        if (y == (SIZE + 1)):
            end_reason = 'RESIGN'
            break
        (board, player) = make_play(x, y, board)
        if conf['SHOW_EACH_MOVE']:
            color = ('W' if (player == 1) else 'B')
            print(('%s(%s,%s)' % (color, x, y)))
            print('')
            print(show_board(board))
            print('')
    (winner, black_points, white_points) = get_winner(board)
    player_string = {1: 'B', 0: 'D', (- 1): 'W'}
    if (end_reason == 'resign'):
        winner_string = ('%s+R' % player_string[player])
    else:
        winner_string = ('%s+%s' % (player_string[winner], abs((black_points - white_points))))
    winner_engine = (engine1 if (winner == 1) else engine2)
    (modelB, modelW) = (model1, model2)
    if conf['SHOW_END_GAME']:
        if (player == (- 1)):
            (bvalue, wvalue) = (value, last_value)
        else:
            (bvalue, wvalue) = (last_value, value)
        print('')
        print(('B:%s, W:%s' % (modelB.name, modelW.name)))
        print(('Bvalue:%s, Wvalue:%s' % (bvalue, wvalue)))
        print(show_board(board))
        print(('Game played (%s: %s) : %s' % (winner_string, end_reason, (datetime.datetime.now() - start))))
    game_data = {'moves': moves, 'modelB_name': modelB.name, 'modelW_name': modelW.name, 'winner': winner, 'winner_model': winner_engine.model.name, 'result': winner_string, 'resign_model1': resign_model1, 'resign_model2': resign_model2}
    return game_data
