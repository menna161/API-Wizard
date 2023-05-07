import numpy as np


def reset(self):
    if (self.IS_EVALUATING or ((self.stack_randomization_range[0] == 0) and (self.stack_randomization_range[1] == 0))):
        self.starting_stack_this_episode = self._base_starting_stack
    else:
        self.starting_stack_this_episode = max(self.poker_env.BIG_BLIND, np.random.randint(low=(self._base_starting_stack - np.abs(self.stack_randomization_range[0])), high=((self._base_starting_stack + self.stack_randomization_range[1]) + 1)))
    self.stack = self.starting_stack_this_episode
    self.hand = []
    self.current_bet = 0
    self.is_allin = False
    self.folded_this_episode = False
    self.has_acted_this_round = False
    self.side_pot_rank = (- 1)
