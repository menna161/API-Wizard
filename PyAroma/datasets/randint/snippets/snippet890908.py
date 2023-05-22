import copy
import unittest
from unittest import TestCase
import numpy as np
from PokerRL.game.games import NoLimitHoldem


def test_get_fraction_of_pot_raise(self):
    for n_plyrs in range(TestPokerEnv.MIN_P, (TestPokerEnv.MAX_P + 1)):
        n = np.random.randint(low=0, high=12)
        for f in [0.1, 0.3, 0.5, 0.7, 1.0, 1.4, 2.2]:
            for _ in range(TestPokerEnv.ITERATIONS):
                env = _get_new_nlh_env(n_plyrs, 100, 1000)
                env.reset()
                for _ in range(n_plyrs):
                    env.step((1, (- 1)))
                last_raiser_id = env.current_player.seat_id
                for _ in range(n):
                    last_raiser_id = env.current_player.seat_id
                    env.step((2, np.random.randint(low=0, high=180)))
                next_raiser_id = env.current_player.seat_id
                suggested_raise = env.get_fraction_of_pot_raise(fraction=f, player_that_bets=env.seats[next_raiser_id])
                s = ((sum(env.side_pots) + env.main_pot) + sum([p.current_bet for p in env.seats]))
                s += (env.seats[last_raiser_id].current_bet - env.seats[next_raiser_id].current_bet)
                last_raiser_tocall_if_next_bets = (suggested_raise - env.seats[last_raiser_id].current_bet)
                should_be = (s * f)
                assert ((should_be - 1) <= last_raiser_tocall_if_next_bets <= (should_be + 1))
