import netomaton as ntm
import numpy as np

if (__name__ == '__main__'):
    '\n    A model of the 1D Diffusion equation: ∂u/∂t = ν ∂²u/∂x²\n\n    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/04_Step_3.ipynb\n    '
    nx = 41
    nt = 99
    dx = (2 / (nx - 1))
    nu = 0.3
    sigma = 0.2
    dt = ((sigma * (dx ** 2)) / nu)
    network = ntm.topology.cellular_automaton(nx)
    initial_conditions = ((([1.0] * 10) + ([2.0] * 11)) + ([1.0] * 20))

    def activity_rule(ctx):
        un_i = ctx.current_activity
        left_label = ((ctx.node_label - 1) % nx)
        un_i_m1 = ctx.activity_of(left_label)
        right_label = ((ctx.node_label + 1) % nx)
        un_i_p1 = ctx.activity_of(right_label)
        return (un_i + (((nu * dt) / (dx ** 2)) * ((un_i_p1 - (2 * un_i)) + un_i_m1)))
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, activity_rule=activity_rule, timesteps=nt)
    ntm.plot_activities(trajectory)
    ntm.animate_plot1D(np.linspace(0, 2, nx), trajectory)
