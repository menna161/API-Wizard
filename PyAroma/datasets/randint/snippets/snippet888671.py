import matplotlib.pylab as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


def sample_action(self, obs):
    'Sample an action for the given observation.\n        \n        Parameters\n        ----------\n        obs: A numpy array of shape [obs_dim].\n        \n        Returns\n        -------\n        An integer, the action sampled.\n        '
    if (np.random.random() < self.epsilon):
        return np.random.randint(self.ac_dim)
    if ((len(obs.shape) != 1) or (obs.shape[0] != self.obs_dim)):
        raise ValueError(('Expected input observation shape [obs_dim], got %s' % str(obs.shape)))
    obs = torch.tensor(obs.reshape(1, (- 1)), dtype=torch.float64)
    return torch.distributions.Categorical(logits=self.eval().double().forward(obs)).sample().item()
