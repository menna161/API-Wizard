import numpy as np
from scipy.special import comb
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange
from PokerRL.game._.cpp_wrappers.CppLUT import CppLibHoldemLuts


def get_n_boards_LUT(self):
    _c = self.get_n_cards_dealt_in_transition_to_LUT()
    return {r: comb(N=(self.rules.N_RANKS * self.rules.N_SUITS), k=_c[r], exact=True, repetition=False) for r in self.rules.ALL_ROUNDS_LIST}
