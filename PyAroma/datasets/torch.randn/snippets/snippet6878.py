import pytest
import numpy as np
import torch
import torch_testing as tt
import gym
from rlil.environments.action import Action, action_decorator


def test_from_list(set_continuous_action_space):
    action1 = Action(torch.randn(1, 2))
    action2 = Action(torch.randn(1, 2))
    action3 = Action(torch.randn(1, 2))
    action = Action.from_list([action1, action2, action3])
    tt.assert_equal(action.raw, torch.cat((action1.raw, action2.raw, action3.raw)))
