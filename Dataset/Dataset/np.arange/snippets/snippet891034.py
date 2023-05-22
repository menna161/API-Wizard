import numpy as np
from scipy.special import comb
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange
from PokerRL.game._.cpp_wrappers.CppLUT import CppLibHoldemLuts


def get_card_in_what_range_idxs_LUT(self):
    return np.arange(self.rules.RANGE_SIZE).reshape((- 1), 1)
