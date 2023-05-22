import torch
from .approximation import Approximation
from rlil.nn import RLNetwork
from rlil.environments import squash_action


def decode_multiple(self, states, num_decode=10):
    z = torch.randn(states.features.size(0), num_decode, self.latent_dim, device=self.device).clamp((- 0.5), 0.5)
    repeated_states = torch.repeat_interleave(states.features.unsqueeze(1), num_decode, 1)
    actions = self.model(torch.cat((repeated_states, z), dim=2))
    return (squash_action(actions, self._tanh_scale, self._tanh_mean), actions)
