import netomaton as ntm
from .rule_test import *


def test_simple_diffusion(self):
    expected = self._convert_to_list_of_lists('simple_diffusion.ca', dtype=float)
    space = np.linspace(25, (- 25), 120)
    initial_conditions = [np.exp((- (x ** 2))) for x in space]
    network = ntm.topology.cellular_automaton(120)
    a = 0.25
    dt = 0.5
    dx = 0.5
    F = ((a * dt) / (dx ** 2))

    def activity_rule(ctx):
        current = ctx.current_activity
        left = ctx.neighbourhood_activities[0]
        right = ctx.neighbourhood_activities[2]
        return (current + (F * ((right - (2 * current)) + left)))
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, activity_rule=activity_rule, timesteps=75)
    activities = ntm.get_activities_over_time_as_list(trajectory)
    np.testing.assert_equal(expected, activities)
