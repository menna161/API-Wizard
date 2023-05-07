import copy
import time
import numpy as np
from gym import spaces
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerEnvStateDictEnums import EnvDictIdxs, PlayerDictIdxs
from PokerRL.game._.rl_env.base._Deck import DeckOfCards
from PokerRL.game._.rl_env.base._PokerPlayer import PokerPlayer


def get_random_action(self):
    a = np.random.randint(low=0, high=3)
    pot_sum = (sum(self.side_pots) + self.main_pot)
    n = int(np.random.normal(loc=(pot_sum / 2), scale=(pot_sum / 5)))
    return (a, n)
