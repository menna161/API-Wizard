from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


def test_init_multiple_relations(self):
    config = [(1, 1, 1), (1, 2), (1, 2), (1, 2), (2, 3), (3, 2)]
    rules = {'in': [('x', 'y')], 'out': [('x', 'y'), ('y', 'z')]}
    model = WolframPhysicsModel(config, rules)
    expected_network = Network()
    expected_network.add_edge(1, 1, label='1', hyperedge_index=0)
    expected_network.add_edge(1, 1, label='1', hyperedge_index=1)
    expected_network.add_edge(1, 2, label='2')
    expected_network.add_edge(1, 2, label='3')
    expected_network.add_edge(1, 2, label='4')
    expected_network.add_edge(3, 2, label='6')
    expected_network.add_edge(2, 3, label='5')
    self.assertEqual(expected_network, model.network)
    self.assertEqual(3, model.last_node)
    self.assertEqual(rules, model.rules)
