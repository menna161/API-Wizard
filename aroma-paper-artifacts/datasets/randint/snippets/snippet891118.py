import numpy as np
import torch
from PokerRL.rl.buffers._circular_base import CircularBufferBase


def sample(self, device, batch_size):
    '\n        Args:\n            batch_size (int)\n            device (torch.device)\n\n        Returns:\n            tuple\n        '
    indices = np.random.randint(low=0, high=self._size, size=batch_size)
    samples = [self._games[i].sample() for i in indices]
    batch_legal_action_mask_tp1 = [sample['mask_tp1'] for sample in samples]
    batch_legal_action_mask_tp1 = torch.from_numpy(np.array(batch_legal_action_mask_tp1)).to(device=device)
    batch_legal_action_mask_t = [sample['mask_t'] for sample in samples]
    batch_legal_action_mask_t = torch.from_numpy(np.array(batch_legal_action_mask_t)).to(device=device)
    batch_action_t = [sample['a'] for sample in samples]
    batch_action_t = torch.tensor(batch_action_t, dtype=torch.long, device=device)
    batch_range_idx = [sample['range_idx'] for sample in samples]
    batch_range_idx = torch.from_numpy(np.array(batch_range_idx)).to(dtype=torch.long, device=device)
    batch_reward = [sample['rew'] for sample in samples]
    batch_reward = torch.from_numpy(np.array(batch_reward)).to(dtype=torch.float32, device=device)
    batch_done = [sample['done'] for sample in samples]
    batch_done = torch.tensor(batch_done, dtype=torch.float32, device=device)
    batch_pub_obs_t = [sample['o_t'] for sample in samples]
    batch_pub_obs_tp1 = [sample['o_tp1'] for sample in samples]
    return (batch_pub_obs_t, batch_action_t, batch_range_idx, batch_legal_action_mask_t, batch_reward, batch_pub_obs_tp1, batch_legal_action_mask_tp1, batch_done)
