import numpy as np
import netomaton as ntm
from .rule_test import *


def test_perturbation_reversible(self):
    np.random.seed(0)
    expected = self._convert_to_list_of_lists('perturbation_reversible.ca')
    network = ntm.topology.cellular_automaton(n=200)
    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(ctx):
        rule = ntm.rules.nks_ca_rule(90)
        if ((ctx.timestep % 10) == 0):
            return 1
        return rule(ctx)
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100, activity_rule=ntm.ReversibleRule(perturbed_rule), past_conditions=[initial_conditions])
    activities = ntm.get_activities_over_time_as_list(trajectory)
    np.testing.assert_almost_equal(expected, activities, decimal=10)
