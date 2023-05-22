import torch
import os
from torch.nn.functional import mse_loss
from .base import Agent, LazyAgent
from copy import deepcopy
from rlil.environments import Action
from rlil.initializer import get_replay_buffer, get_device, get_writer
from rlil.utils import Samples


def train(self):
    if self.should_train():
        (states, actions, rewards, next_states, _, _) = self.replay_buffer.get_all_transitions()
        features = self.feature_nw.target(states)
        values = self.v.target(features)
        next_values = self.v.target(self.feature_nw.target(next_states))
        advantages = self.replay_buffer.compute_gae(rewards, values, next_values, next_states.mask)
        pi_0 = self.policy.no_grad(features).log_prob(actions.raw)
        targets = (values + advantages)
        for _ in range(self.epochs):
            minibatch_size = int((len(states) / self.minibatches))
            indexes = torch.randperm(len(states))
            for n in range(self.minibatches):
                first = (n * minibatch_size)
                last = (first + minibatch_size)
                i = indexes[first:last]
                self._train_minibatch(states[i], actions[i], pi_0[i], advantages[i], targets[i])
                self.writer.train_steps += 1
        self.replay_buffer.clear()
