from abc import ABC, abstractmethod
import numpy as np
import torch
from rlil.environments import State, Action
from rlil.initializer import get_device, is_debug_mode
from .replay_buffer import ExperienceReplayBuffer
from .base import BaseBufferWrapper
from .gae_wrapper import GaeWrapper


def sample(self, batch_size):
    batch_size = int((batch_size / 2))
    (states, actions, rewards, next_states, weights, indexes) = self.buffer.sample(batch_size)
    (exp_states, exp_actions, exp_rewards, exp_next_states, exp_weights, exp_indexes) = self.expert_buffer.sample(batch_size)
    rewards = torch.zeros_like(rewards, dtype=torch.float32, device=self.device)
    exp_rewards = torch.ones_like(exp_rewards, dtype=torch.float32, device=self.device)
    states = State.from_list([states, exp_states])
    actions = Action.from_list([actions, exp_actions])
    rewards = torch.cat([rewards, exp_rewards], axis=0)
    next_states = State.from_list([next_states, exp_next_states])
    weights = torch.cat([weights, exp_weights], axis=0)
    index = torch.randperm(len(rewards))
    if ((indexes is None) or (exp_indexes is None)):
        indexes = None
    else:
        indexes = torch.cat([indexes, exp_indexes], axis=0)[index]
    return (states[index], actions[index], rewards[index], next_states[index], weights[index], indexes)
