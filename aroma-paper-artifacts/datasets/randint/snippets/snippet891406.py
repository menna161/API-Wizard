import time
import numpy as np
from PokerRL.game.Poker import Poker
from PokerRL.game._.rl_env.base.PokerEnv import PokerEnv as _PokerEnv
from PokerRL.game.poker_env_args import DiscretizedPokerEnvArgs


def _get_env_adjusted_action_formulation(self, action_int):
    '\n\n        Args:\n            action_int: integer representation of discretized action\n\n        Returns:\n            list: (action, raise_size) in "continuous" PokerEnv format\n\n        '
    if (action_int == 0):
        return [0, (- 1)]
    if (action_int == 1):
        return [1, (- 1)]
    elif (action_int > 1):
        selected = self.get_fraction_of_pot_raise(fraction=self.bet_sizes_list_as_frac_of_pot[(action_int - 2)], player_that_bets=self.current_player)
        if (self.uniform_action_interpolation and (not self.IS_EVALUATING)):
            if (action_int == (self.N_ACTIONS - 1)):
                if self.IS_POT_LIMIT_GAME:
                    max_amnt = self.get_fraction_of_pot_raise(fraction=1.0, player_that_bets=self.current_player)
                elif self.IS_FIXED_LIMIT_GAME:
                    raise EnvironmentError('Should not get here with a limit game!')
                else:
                    max_amnt = (self.current_player.stack + self.current_player.current_bet)
            else:
                bigger = self.get_fraction_of_pot_raise(fraction=self.bet_sizes_list_as_frac_of_pot[(action_int - 1)], player_that_bets=self.current_player)
                max_amnt = int((float((selected + bigger)) / 2))
            if (action_int == 2):
                min_amnt = self._get_current_total_min_raise()
            else:
                smaller = self.get_fraction_of_pot_raise(fraction=self.bet_sizes_list_as_frac_of_pot[(action_int - 3)], player_that_bets=self.current_player)
                min_amnt = int((float((selected + smaller)) / 2))
            if (min_amnt >= max_amnt):
                return [2, min_amnt]
            return [2, np.random.randint(low=min_amnt, high=max_amnt)]
        else:
            return [2, selected]
    else:
        raise ValueError(action_int)
