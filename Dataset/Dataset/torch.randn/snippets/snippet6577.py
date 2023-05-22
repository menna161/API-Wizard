import torch
from .approximation import Approximation
from rlil.nn import RLNetwork
from rlil.environments import squash_action


def forward(self, states, z=None):
    if (z is None):
        z = torch.randn(states.features.size(0), self.latent_dim, device=self.device).clamp((- 0.5), 0.5)
    actions = self.model(torch.cat((states.features, z), dim=1))
    return squash_action(actions, self._tanh_scale, self._tanh_mean)
