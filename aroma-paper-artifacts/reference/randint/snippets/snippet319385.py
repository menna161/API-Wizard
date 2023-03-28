import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import argparse
import os
import time
import copy
from gym import wrappers
import matplotlib.pyplot as plt
from helpers import argmax, check_space, is_atari_game, copy_atari_state, store_safely, restore_atari_state, stable_normalizer, smooth, symmetric_remove, Database
from rl.make_game import make_game


def agent(game, n_ep, n_mcts, max_ep_len, lr, c, gamma, data_size, batch_size, temp, n_hidden_layers, n_hidden_units):
    ' Outer training loop '
    episode_returns = []
    timepoints = []
    Env = make_game(game)
    is_atari = is_atari_game(Env)
    mcts_env = (make_game(game) if is_atari else None)
    D = Database(max_size=data_size, batch_size=batch_size)
    model = Model(Env=Env, lr=lr, n_hidden_layers=n_hidden_layers, n_hidden_units=n_hidden_units)
    t_total = 0
    R_best = (- np.Inf)
    with tf.Session() as sess:
        model.sess = sess
        sess.run(tf.global_variables_initializer())
        for ep in range(n_ep):
            start = time.time()
            s = Env.reset()
            R = 0.0
            a_store = []
            seed = np.random.randint(10000000.0)
            Env.seed(seed)
            if is_atari:
                mcts_env.reset()
                mcts_env.seed(seed)
            mcts = MCTS(root_index=s, root=None, model=model, na=model.action_dim, gamma=gamma)
            for t in range(max_ep_len):
                mcts.search(n_mcts=n_mcts, c=c, Env=Env, mcts_env=mcts_env)
                (state, pi, V) = mcts.return_results(temp)
                D.store((state, V, pi))
                a = np.random.choice(len(pi), p=pi)
                a_store.append(a)
                (s1, r, terminal, _) = Env.step(a)
                R += r
                t_total += n_mcts
                if terminal:
                    break
                else:
                    mcts.forward(a, s1)
            episode_returns.append(R)
            timepoints.append(t_total)
            store_safely(os.getcwd(), 'result', {'R': episode_returns, 't': timepoints})
            if (R > R_best):
                a_best = a_store
                seed_best = seed
                R_best = R
            print('Finished episode {}, total return: {}, total time: {} sec'.format(ep, np.round(R, 2), np.round((time.time() - start), 1)))
            D.reshuffle()
            for epoch in range(1):
                for (sb, Vb, pib) in D:
                    model.train(sb, Vb, pib)
    return (episode_returns, timepoints, a_best, seed_best, R_best)
