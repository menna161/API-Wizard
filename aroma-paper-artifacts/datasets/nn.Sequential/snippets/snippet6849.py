import unittest
import torch
import gym
from torch import nn
from torch.nn.functional import smooth_l1_loss
import torch_testing as tt
import numpy as np
from rlil.environments import State, Action
from rlil.approximation import QNetwork, FixedTarget


def test_target_net(self):
    torch.manual_seed(2)
    model = nn.Sequential(nn.Linear(1, 1))
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
    q = QNetwork(model, optimizer, target=FixedTarget(3))
    inputs = State(torch.tensor([1.0]).unsqueeze(0))

    def loss(policy_value):
        target = (policy_value - 1)
        return smooth_l1_loss(policy_value, target.detach())
    policy_value = q(inputs)
    target_value = q.target(inputs).item()
    np.testing.assert_equal(policy_value.item(), (- 0.008584141731262207))
    np.testing.assert_equal(target_value, (- 0.008584141731262207))
    q.reinforce(loss(policy_value))
    policy_value = q(inputs)
    target_value = q.target(inputs).item()
    np.testing.assert_equal(policy_value.item(), (- 0.20858412981033325))
    np.testing.assert_equal(target_value, (- 0.008584141731262207))
    q.reinforce(loss(policy_value))
    policy_value = q(inputs)
    target_value = q.target(inputs).item()
    np.testing.assert_equal(policy_value.item(), (- 0.4085841178894043))
    np.testing.assert_equal(target_value, (- 0.008584141731262207))
    q.reinforce(loss(policy_value))
    policy_value = q(inputs)
    target_value = q.target(inputs).item()
    np.testing.assert_equal(policy_value.item(), (- 0.6085841655731201))
    np.testing.assert_equal(target_value, (- 0.6085841655731201))
    q.reinforce(loss(policy_value))
    policy_value = q(inputs)
    target_value = q.target(inputs).item()
    np.testing.assert_equal(policy_value.item(), (- 0.8085841536521912))
    np.testing.assert_equal(target_value, (- 0.6085841655731201))
