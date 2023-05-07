from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_config_interconversion(self):
    expected = [(1, 1, 3), (1, 3, 2), (1, 2, 4), (2, 4, 1)]
    network = WolframPhysicsModel(expected, {}).network
    actual = WolframPhysicsModel.network_to_config(network)
    self.assertEqual(actual, expected)
