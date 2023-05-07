import copy
import unittest
from unittest import TestCase
import numpy as np
from PokerRL.game.games import NoLimitHoldem


def test_get_filtered_action_but_change_nothing(self):
    env = _get_new_nlh_env(7, 100, 1000)
    env.reset()
    for _ in range(TestPokerEnv.ITERATIONS):
        orig_action = (np.random.randint(low=0, high=2), np.random.randint(low=0, high=env.MAX_CHIPS))
        _orig_action = copy.deepcopy(orig_action)
        a = env._get_fixed_action(action=orig_action)
        (obs, rew, terminal, _) = env.step(action=tuple(a))
        if terminal:
            env.reset()
        assert (orig_action == _orig_action)
