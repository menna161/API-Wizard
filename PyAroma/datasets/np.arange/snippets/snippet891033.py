import numpy as np
from scipy.special import comb
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange
from PokerRL.game._.cpp_wrappers.CppLUT import CppLibHoldemLuts


def get_hole_card_2_idx_LUT(self):
    return np.expand_dims(np.arange(self.rules.N_CARDS_IN_DECK), axis=1)
