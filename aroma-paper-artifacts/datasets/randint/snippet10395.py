import numpy as np
import netomaton as ntm
from .rule_test import *


def test_perturbation_eca(self):
    np.random.seed(0)
    expected = self._convert_to_list_of_lists('perturbation_eca.ca')
    network = ntm.topology.cellular_automaton(n=200)
    initial_conditions = ((([0] * 100) + [1]) + ([0] * 99))

    def perturb(pctx):
        '\n            Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.\n            '
        if (pctx.node_label == 100):
            return np.random.randint(2)
        return pctx.node_activity
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100, activity_rule=ntm.rules.nks_ca_rule(30), perturbation=perturb)
    activities = ntm.get_activities_over_time_as_list(trajectory)
    np.testing.assert_almost_equal(expected, activities, decimal=10)
