import unittest
from unittest import TestCase
import numpy as np
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange
from PokerRL.game.games import DiscretizedNLHoldem, DiscretizedNLLeduc
from PokerRL.game.wrappers import VanillaEnvBuilder


def test_get_possible_range_idxs_leduc(self):
    for n in range(2, 9):
        env_bldr = get_leduc_env_bldr()
        for c in range(env_bldr.rules.N_CARDS_IN_DECK):
            board_2d = env_bldr.lut_holder.get_2d_cards(np.array([c], dtype=np.int32))
            result = PokerRange.get_possible_range_idxs(rules=env_bldr.rules, lut_holder=env_bldr.lut_holder, board_2d=board_2d)
            should_be = np.delete(np.arange(env_bldr.rules.RANGE_SIZE, dtype=np.int32), c)
            assert np.array_equal(a1=result, a2=should_be)
        board_2d = np.array([Poker.CARD_NOT_DEALT_TOKEN_2D], dtype=np.int8)
        result = PokerRange.get_possible_range_idxs(rules=env_bldr.rules, lut_holder=env_bldr.lut_holder, board_2d=board_2d)
        should_be = np.arange(env_bldr.rules.RANGE_SIZE, dtype=np.int32)
        assert np.array_equal(a1=result, a2=should_be)
