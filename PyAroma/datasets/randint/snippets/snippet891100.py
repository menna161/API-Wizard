import numpy as np
from PokerRL.rl import rl_util
from PokerRL.rl.buffers._circular_base import BRMemorySaverBase


def sample(self):
    idx = np.random.randint(low=0, high=self._n_steps_in_game_memory)
    return {'o_t': self._obs_sequence[:self._obs_t_idxs_per_step[idx]], 'o_tp1': self._obs_sequence[:self._obs_tp1_idxs_per_step[idx]], 'mask_t': self._legal_actions_mask_t_buffer[idx], 'mask_tp1': self._legal_actions_mask_tp1_buffer[idx], 'a': self._action_buffer[idx], 'rew': self._reward_buffer[idx], 'done': self._done_buffer[idx], 'range_idx': self._range_idx}
