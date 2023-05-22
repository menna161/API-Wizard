from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_config_interconversion2(self):
    expected = [(4, 2), (2, 3), (5, 1), (1, 2)]
    network = WolframPhysicsModel(expected, {}).network
    actual = WolframPhysicsModel.network_to_config(network)
    self.assertEqual(actual, expected)
