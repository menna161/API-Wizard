import os.path
import torch
import numpy as np
from alpha_net_c4 import ConnectNet
from connect_board import board as cboard
import encoder_decoder_c4 as ed
import copy
from MCTS_c4 import UCT_search, do_decode_n_move_pieces, get_policy
import pickle
import torch.multiprocessing as mp
import datetime
import logging


def evaluate(self, num_games, cpu):
    current_wins = 0
    logger.info(('[CPU %d]: Starting games...' % cpu))
    for i in range(num_games):
        with torch.no_grad():
            (winner, dataset) = self.play_round()
            print(('%s wins!' % winner))
        if (winner == 'current'):
            current_wins += 1
        save_as_pickle(('evaluate_net_dataset_cpu%i_%i_%s_%s' % (cpu, i, datetime.datetime.today().strftime('%Y-%m-%d'), str(winner))), dataset)
    print(('Current_net wins ratio: %.5f' % (current_wins / num_games)))
    save_as_pickle(('wins_cpu_%i' % cpu), {'best_win_ratio': (current_wins / num_games), 'num_games': num_games})
    logger.info(('[CPU %d]: Finished arena games!' % cpu))
