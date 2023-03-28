import pickle
import os
import collections
import numpy as np
import math
import encoder_decoder_c4 as ed
from connect_board import board as c_board
import copy
import torch
import torch.multiprocessing as mp
from alpha_net_c4 import ConnectNet
import datetime
import logging
from tqdm import tqdm


def MCTS_self_play(connectnet, num_games, start_idx, cpu, args, iteration):
    logger.info(('[CPU: %d]: Starting MCTS self-play...' % cpu))
    if (not os.path.isdir(('./datasets/iter_%d' % iteration))):
        if (not os.path.isdir('datasets')):
            os.mkdir('datasets')
        os.mkdir(('datasets/iter_%d' % iteration))
    for idxx in tqdm(range(start_idx, (num_games + start_idx))):
        logger.info(('[CPU: %d]: Game %d' % (cpu, idxx)))
        current_board = c_board()
        checkmate = False
        dataset = []
        states = []
        value = 0
        move_count = 0
        while ((checkmate == False) and (current_board.actions() != [])):
            if (move_count < 11):
                t = args.temperature_MCTS
            else:
                t = 0.1
            states.append(copy.deepcopy(current_board.current_board))
            board_state = copy.deepcopy(ed.encode_board(current_board))
            root = UCT_search(current_board, 777, connectnet, t)
            policy = get_policy(root, t)
            print(('[CPU: %d]: Game %d POLICY:\n ' % (cpu, idxx)), policy)
            current_board = do_decode_n_move_pieces(current_board, np.random.choice(np.array([0, 1, 2, 3, 4, 5, 6]), p=policy))
            dataset.append([board_state, policy])
            print(('[Iteration: %d CPU: %d]: Game %d CURRENT BOARD:\n' % (iteration, cpu, idxx)), current_board.current_board, current_board.player)
            print(' ')
            if (current_board.check_winner() == True):
                if (current_board.player == 0):
                    value = (- 1)
                elif (current_board.player == 1):
                    value = 1
                checkmate = True
            move_count += 1
        dataset_p = []
        for (idx, data) in enumerate(dataset):
            (s, p) = data
            if (idx == 0):
                dataset_p.append([s, p, 0])
            else:
                dataset_p.append([s, p, value])
        del dataset
        save_as_pickle((('iter_%d/' % iteration) + ('dataset_iter%d_cpu%i_%i_%s' % (iteration, cpu, idxx, datetime.datetime.today().strftime('%Y-%m-%d')))), dataset_p)
