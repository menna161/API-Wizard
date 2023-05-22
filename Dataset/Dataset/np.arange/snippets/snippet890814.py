import numpy as np
from PokerRL.game.Poker import Poker


@staticmethod
def get_range_size(n_hole_cards, n_cards_in_deck):
    '\n        Args:\n            n_hole_cards:       number of cards each player is dealt\n            n_cards_in_deck:    number of unique cards in the deck\n\n        Returns:\n            int:                the number of possible hands (order of cards does not matter) given a set number of\n                                holecards and cards in the deck.\n        '
    range_size = 1
    for i in range(n_hole_cards):
        range_size *= (n_cards_in_deck - i)
    n_hc_factorial = np.prod(np.arange(1, (n_hole_cards + 1)))
    return int((range_size / n_hc_factorial))
