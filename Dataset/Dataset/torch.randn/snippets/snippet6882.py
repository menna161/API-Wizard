import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil.environments.action import Action, action_decorator


def test_len():
    action_space = gym.spaces.Box(low=np.array([(- 1), (- 2), (- 3), (- 4)]), high=np.array([1, 2, 3, 4]))
    Action.set_action_space(action_space)
    action = Action(torch.randn(3, 4))
    assert (len(action) == 3)
