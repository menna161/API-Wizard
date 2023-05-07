import copy
import unittest
from unittest import TestCase
import numpy as np
from PokerRL.game.games import NoLimitHoldem


def test_get_frac_from_chip_amt(self):
    for i in range(self.ITERATIONS):
        for n_plyrs in range(TestPokerEnv.MIN_P, (TestPokerEnv.MAX_P + 1)):
            n = np.random.randint(low=0, high=2)
            for amt in [10, 233, 412, 5001]:
                env = _get_new_nlh_env(n_plyrs, 300, 1000)
                env.reset()
                for _ in range(n_plyrs):
                    env.step((1, (- 1)))
                for _ in range(n):
                    env.step((2, np.random.randint(low=0, high=255)))
                    if (np.random.random() > 0.5):
                        env.step((1, (- 1)))
                next_raiser_id = env.current_player.seat_id
                frac = env.get_frac_from_chip_amt(amt=amt, player_that_bets=env.seats[next_raiser_id])
                suggested_raise = env.get_fraction_of_pot_raise(fraction=frac, player_that_bets=env.seats[next_raiser_id])
                assert np.allclose(amt, suggested_raise, atol=1.1)
