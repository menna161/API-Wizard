import time
import numpy as np
from PokerRL.game.Poker import Poker
from PokerRL.game._.rl_env.base.PokerEnv import PokerEnv as _PokerEnv
from PokerRL.game.poker_env_args import DiscretizedPokerEnvArgs


def get_random_action(self):
    legal = self.get_legal_actions()
    return legal[np.random.randint(len(legal))]
