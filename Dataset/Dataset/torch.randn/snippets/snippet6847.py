import unittest
import torch
import gym
from torch import nn
from torch.nn.functional import smooth_l1_loss
import torch_testing as tt
import numpy as np
from rlil.environments import State, Action
from rlil.approximation import QNetwork, FixedTarget


def test_eval_list(self):
    states = State(torch.randn(5, STATE_DIM), mask=torch.tensor([1, 1, 0, 1, 0]))
    result = self.q.eval(states)
    tt.assert_almost_equal(result, torch.tensor([[(- 0.238509), (- 0.726287), (- 0.034026)], [(- 0.35688755), (- 0.6612102), 0.34849477], [0.0, 0.0, 0.0], [0.1944, (- 0.5536), (- 0.2345)], [0.0, 0.0, 0.0]]), decimal=2)
