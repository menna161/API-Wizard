import unittest
import numpy as np
import torch
from rlil import nn
from rlil.environments import Action
from rlil.policies.deterministic import DeterministicPolicyNetwork
from rlil.memory import ExperienceReplayBuffer
from rlil.initializer import get_replay_buffer, get_n_step
from rlil.utils import Samples


def __init__(self, env):
    model = nn.Sequential(nn.Flatten(), nn.Linear(env.state_space.shape[0], Action.action_space().shape[0]))
    self.policy_model = DeterministicPolicyNetwork(model, Action.action_space())
    self._state = None
    self._action = None
    self.replay_buffer = get_replay_buffer()
