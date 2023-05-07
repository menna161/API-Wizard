from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_init_binary_relation(self):
    config = [(1, 2)]
    rules = {'in': [('x', 'y')], 'out': [('x', 'y'), ('y', 'z')]}
    model = WolframPhysicsModel(config, rules)
    expected_network = Network()
    expected_network.add_edge(1, 2, label='1')
    self.assertEqual(expected_network, model.network)
    self.assertEqual(2, model.last_node)
    self.assertEqual(rules, model.rules)
