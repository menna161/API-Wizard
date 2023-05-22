import numpy as np
from PokerRL.game.Poker import Poker


@staticmethod
def get_possible_range_idxs(rules, lut_holder, board_2d):
    arr = np.arange(rules.RANGE_SIZE)
    if (board_2d.shape[0] == 0):
        return arr
    lut_holder.get_1d_cards(cards_2d=board_2d)
    blocked_cards_1d = np.array([c for c in lut_holder.get_1d_cards(cards_2d=board_2d) if (c != Poker.CARD_NOT_DEALT_TOKEN_1D)])
    if (rules.N_HOLE_CARDS == 1):
        arr = np.delete(arr, obj=blocked_cards_1d)
        return arr
    elif (rules.N_HOLE_CARDS == 2):
        hands = []
        for c in blocked_cards_1d:
            for c1 in range(0, c):
                hands.append(lut_holder.get_range_idx_from_hole_cards(lut_holder.get_2d_cards(np.array([c1, c], dtype=np.int8))))
            for c2 in range((c + 1), rules.N_CARDS_IN_DECK):
                hands.append(lut_holder.get_range_idx_from_hole_cards(lut_holder.get_2d_cards(np.array([c, c2], dtype=np.int8))))
        blocked_idxs = np.unique(np.array(hands))
        arr = np.delete(arr, obj=blocked_idxs)
        return arr
    else:
        raise NotImplementedError(('self.N_HOLE_CARDS > 2:  ' + str(rules.N_HOLE_CARDS)))
