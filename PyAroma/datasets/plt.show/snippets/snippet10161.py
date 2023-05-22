import networkx as nx
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll
import collections
from .state import State
from .substitution_system import SubstitutionSystem
import cPickle as pickle
import pickle


def animate_plot1D(x, y, save=False, interval=50, dpi=80):
    if isinstance(y[0], State):
        y = get_activities_over_time_as_list(y)
    fig1 = plt.figure()
    (line,) = plt.plot(x, y[0])

    def update_line(activity):
        line.set_data(x, activity)
        return (line,)
    ani = animation.FuncAnimation(fig1, update_line, frames=y, blit=True, interval=interval)
    if save:
        ani.save('plot.gif', dpi=dpi, writer='imagemagick')
    plt.show()
