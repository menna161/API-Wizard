from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_init_large_hyperedge(self):
    config = [(3, 1, 2, 1, 1, 4, 1, 1)]
    rules = {'in': [('x', 'y')], 'out': [('x', 'y'), ('y', 'z')]}
    model = WolframPhysicsModel(config, rules)
    expected_network = Network()
    expected_network.add_edge(3, 1, label='1', hyperedge_index=0)
    expected_network.add_edge(1, 2, label='1', hyperedge_index=1)
    expected_network.add_edge(2, 1, label='1', hyperedge_index=2)
    expected_network.add_edge(1, 1, label='1', hyperedge_index=3)
    expected_network.add_edge(1, 4, label='1', hyperedge_index=4)
    expected_network.add_edge(4, 1, label='1', hyperedge_index=5)
    expected_network.add_edge(1, 1, label='1', hyperedge_index=6)
    self.assertEqual(expected_network, model.network)
    self.assertEqual(4, model.last_node)
    self.assertEqual(rules, model.rules)
