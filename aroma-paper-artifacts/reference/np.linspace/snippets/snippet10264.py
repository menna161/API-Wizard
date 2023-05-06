import netomaton as ntm
from .rule_test import *


def test_wave_equation(self):
    expected = self._convert_to_list_of_lists('wave_equation.ca', dtype=float)
    nx = 401
    nt = 255
    dx = 0.1
    dt = 0.05
    space = np.linspace(20, (- 20), nx)
    initial_conditions = [np.exp((- (x ** 2))) for x in space]
    network = ntm.topology.cellular_automaton(nx)

    def activity_rule(ctx):
        un_i = ctx.current_activity
        left_label = ((ctx.node_label - 1) % nx)
        un_i_m1 = ctx.activity_of(left_label)
        right_label = ((ctx.node_label + 1) % nx)
        un_i_p1 = ctx.activity_of(right_label)
        un_m1_i = ctx.past_activity_of(ctx.node_label)
        return ((((dt ** 2) * ((un_i_p1 - (2 * un_i)) + un_i_m1)) / (dx ** 2)) + ((2 * un_i) - un_m1_i))
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, activity_rule=activity_rule, timesteps=nt, past_conditions=[initial_conditions])
    activities = ntm.get_activities_over_time_as_list(trajectory)
    np.testing.assert_equal(expected, activities)
