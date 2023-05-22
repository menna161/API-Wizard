import copy
import time
import numpy as np
from gym import spaces
from PokerRL.game.Poker import Poker
from PokerRL.game.PokerEnvStateDictEnums import EnvDictIdxs, PlayerDictIdxs
from PokerRL.game._.rl_env.base._Deck import DeckOfCards
from PokerRL.game._.rl_env.base._PokerPlayer import PokerPlayer


def _payout_pots(self):
    self._assign_hand_ranks_to_all_players()
    if (self.N_SEATS == 2):
        if (self.seats[0].hand_rank > self.seats[1].hand_rank):
            self.seats[0].award(self.main_pot)
        elif (self.seats[0].hand_rank < self.seats[1].hand_rank):
            self.seats[1].award(self.main_pot)
        else:
            self.seats[0].award((self.main_pot / 2))
            self.seats[1].award((self.main_pot / 2))
        self.main_pot = 0
    else:
        pots = np.array(([self.main_pot] + self.side_pots))
        pot_ranks = np.arange(start=(- 1), stop=len(self.side_pots))
        pot_and_pot_ranks = np.array((pots, pot_ranks)).T
        for e in pot_and_pot_ranks:
            pot = e[0]
            rank = e[1]
            eligible_players = [p for p in self.seats if ((p.side_pot_rank >= rank) and (not p.folded_this_episode))]
            num_eligible = len(eligible_players)
            if (num_eligible > 0):
                winner_list = self._get_winner_list(players_to_consider=eligible_players)
                num_winners = int(len(winner_list))
                chips_per_winner = int((pot / num_winners))
                num_non_div_chips = (int(pot) % num_winners)
                for p in winner_list:
                    p.award(chips_per_winner)
                shuffled_winner_idxs = np.arange(num_winners)
                np.random.shuffle(shuffled_winner_idxs)
                for p_idx in shuffled_winner_idxs[:num_non_div_chips]:
                    self.seats[p_idx].award(1)
        self.side_pots = ([0] * self.N_SEATS)
        self.main_pot = 0
