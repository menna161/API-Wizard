import torch
from PokerRL.rl.buffers._circular_base import CircularBufferBase


def sample(self, device, batch_size):
    indices = torch.randint(0, self._size, (batch_size,), dtype=torch.long, device=device)
    return (self._pub_obs_t_buffer[indices].to(device), self._action_t_buffer[indices].to(device), self._range_idx_buffer[indices].to(device), self._legal_action_mask_t_buffer[indices].to(device), self._reward_buffer[indices].to(device), self._pub_obs_tp1_buffer[indices].to(device), self._legal_action_mask_tp1_buffer[indices].to(device), self._done_buffer[indices].to(device))
