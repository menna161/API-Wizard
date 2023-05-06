import netomaton as ntm
import numpy as np

if (__name__ == '__main__'):
    "\n    Simulates the Wave Equation:\n\n    ∂²u/∂t² = ∂²u/∂x²\n\n    Reproduces the middle plot of Wolfram's NKS, page 163. \n\n    See: https://www.wolframscience.com/nks/p163--partial-differential-equations/\n    "
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
    ntm.plot_activities(trajectory)
    ntm.animate_plot1D(np.linspace(0, 2, nx), trajectory)
