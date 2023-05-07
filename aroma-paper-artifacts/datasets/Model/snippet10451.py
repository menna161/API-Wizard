from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_init_multiple_ternary_relations(self):
    config = [(1, 1, 1), (1, 2, 3), (3, 4, 4)]
    rules = {'in': [('x', 'y')], 'out': [('x', 'y'), ('y', 'z')]}
    model = WolframPhysicsModel(config, rules)
    expected_network = Network()
    expected_network.add_edge(1, 1, label='1', hyperedge_index=0)
    expected_network.add_edge(1, 1, label='1', hyperedge_index=1)
    expected_network.add_edge(1, 2, label='2', hyperedge_index=0)
    expected_network.add_edge(2, 3, label='2', hyperedge_index=1)
    expected_network.add_edge(3, 4, label='3', hyperedge_index=0)
    expected_network.add_edge(4, 4, label='3', hyperedge_index=1)
    self.assertEqual(expected_network, model.network)
    self.assertEqual(4, model.last_node)
    self.assertEqual(rules, model.rules)
