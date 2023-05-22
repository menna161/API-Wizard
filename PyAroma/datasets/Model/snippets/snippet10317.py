import netomaton as ntm
from .rule_test import *
import numpy as np


def test_fungal_growth(self):
    R_E = 80000.0
    timesteps = 10
    width = 10
    height = 10
    initial_conditions = ntm.init_simple2d(width, height, val=R_E, dtype=float)
    model = ntm.FungalGrowthModel(R_E, width, height, initial_conditions, seed=20210408, verbose=False)
    trajectory = ntm.evolve(network=model.network, initial_conditions=initial_conditions, activity_rule=model.activity_rule, topology_rule=model.topology_rule, update_order=model.update_order, timesteps=timesteps)
    activities_list = ntm.get_activities_over_time_as_list(trajectory)
    expected = self._convert_to_list_of_lists('fungal_growth.ca', dtype=float)
    np.testing.assert_almost_equal(expected, activities_list, decimal=11)
    expected = self._convert_from_literal('fungal_growth_model.txt')
    actual = {i: state.network.to_dict() for (i, state) in enumerate(trajectory)}
    self.assertEqual(expected, actual)
