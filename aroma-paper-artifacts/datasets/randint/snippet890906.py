import copy
import unittest
from unittest import TestCase
import numpy as np
from PokerRL.game.games import NoLimitHoldem


def test_get_and_set_env(self):
    for n in range(TestPokerEnv.MIN_P, (TestPokerEnv.MAX_P + 1)):
        env = _get_new_nlh_env(n, 100, 1000, True)
        env.reset()
        for _ in range(TestPokerEnv.ITERATIONS):
            repeat_cause_terminal = True
            while repeat_cause_terminal:
                (o_obs, reward, terminal, info) = env.reset()
                i = 0
                while ((not terminal) and (i < np.random.randint(low=0, high=(n * 6)))):
                    (o_obs, reward, terminal, info) = env.step(env.get_random_action())
                    i += 1
                    repeat_cause_terminal = terminal
            saved_state = env.state_dict()
            i = 0
            while ((not terminal) and (i < np.random.randint(low=0, high=(n * 4)))):
                (obs, reward, terminal, info) = env.step(action=env.get_random_action())
                i += 1
            env.load_state_dict(saved_state)
            obs = env.get_current_obs(False)
            np.array_equal(obs, o_obs)
            env.reset()
