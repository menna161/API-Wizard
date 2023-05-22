import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil.environments.action import Action, action_decorator


def test_continuous_action(set_continuous_action_space):
    raw = torch.tensor([[0, 0], [2, 2], [(- 20), (- 20)]], dtype=torch.float32)
    action = Action(raw)
    tt.assert_equal(action.raw, raw)
    tt.assert_equal(action.features, torch.tensor([[0, 0], [1, 2], [(- 1), (- 10)]], dtype=torch.float32))
    with pytest.raises(AssertionError):
        raw = torch.randn(3, 5)
        action = Action(raw)
