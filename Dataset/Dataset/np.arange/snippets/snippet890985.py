import numpy as np
import torch
from PokerRL.eval.lbr import _util
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerRange import PokerRange


def __init__(self, t_prof, env_bldr, env, lbr_hand_2d):
    self.t_prof = t_prof
    self.env_bldr = env_bldr
    self._bigger_idxs = []
    self._equal_idxs = []
    self._env = env
    self._lbr_hand_1d = self.env_bldr.lut_holder.get_1d_cards(cards_2d=lbr_hand_2d)
    self._lbr_hand_range_idx = self.env_bldr.lut_holder.get_range_idx_from_hole_cards(hole_cards_2d=lbr_hand_2d)
    self._board_2d = np.copy(self._env.board)
    self._board_1d = self.env_bldr.lut_holder.get_1d_cards(self._board_2d)
    self._cards_dealt = np.array([c for c in self._board_1d if (c != Poker.CARD_NOT_DEALT_TOKEN_1D)])
    self._possible_cards = np.arange(self.env_bldr.rules.N_CARDS_IN_DECK, dtype=np.int32)
    self._possible_cards = np.delete(self._possible_cards, np.concatenate((self._cards_dealt, self._lbr_hand_1d)))
    self._n_cards_to_deal = (env_bldr.lut_holder.DICT_LUT_N_CARDS_OUT[self._env.ALL_ROUNDS_LIST[(- 1)]] - env_bldr.lut_holder.DICT_LUT_N_CARDS_OUT[self._env.current_round])
    self._build_eq_vecs(board_1d=np.copy(self._board_1d), n_cards_to_deal=self._n_cards_to_deal, possible_cards_1d=np.copy(self._possible_cards))
