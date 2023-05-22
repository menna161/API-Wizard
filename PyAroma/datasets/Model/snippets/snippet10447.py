from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_init_ternary_self_looping_relation(self):
    config = [(1, 1, 1)]
    rules = {'in': [('x', 'y')], 'out': [('x', 'y'), ('y', 'z')]}
    model = WolframPhysicsModel(config, rules)
    expected_network = Network()
    expected_network.add_edge(1, 1, label='1', hyperedge_index=0)
    expected_network.add_edge(1, 1, label='1', hyperedge_index=1)
    self.assertEqual(expected_network, model.network)
    self.assertEqual(1, model.last_node)
    self.assertEqual(rules, model.rules)
