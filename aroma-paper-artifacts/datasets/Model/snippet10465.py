from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_config_interconversion3(self):
    expected = [(1, 1, 1), (1, 2), (1, 2), (1, 2), (2, 3), (3, 2)]
    network = WolframPhysicsModel(expected, {}).network
    actual = WolframPhysicsModel.network_to_config(network)
    self.assertEqual(actual, expected)
