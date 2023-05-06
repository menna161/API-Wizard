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


def animate_activities(trajectory_or_activities, title='', shape=None, save=False, interval=50, colormap='Greys', vmin=None, vmax=None, show_grid=False, show_margin=True, scale=0.6, dpi=80, blit=True, with_timestep=False):
    if (len(trajectory_or_activities) is 0):
        raise Exception('there are no activities')
    if isinstance(trajectory_or_activities[0], State):
        activities = get_activities_over_time_as_list(trajectory_or_activities)
    else:
        activities = trajectory_or_activities
    if (shape is not None):
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    (fig, ax) = plt.subplots()
    title_text = plt.title(title)
    if (not show_margin):
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    grid_linewidth = 0.0
    if show_grid:
        plt.xticks(np.arange((- 0.5), len(activities[0][0]), 1), '')
        plt.yticks(np.arange((- 0.5), len(activities[0]), 1), '')
        plt.tick_params(axis='both', which='both', length=0)
        grid_linewidth = 0.5
    vertical = np.arange((- 0.5), len(activities[0][0]), 1)
    horizontal = np.arange((- 0.5), len(activities[0]), 1)
    lines = ([[(x, y) for y in ((- 0.5), horizontal[(- 1)])] for x in vertical] + [[(x, y) for x in ((- 0.5), vertical[(- 1)])] for y in horizontal])
    grid = mcoll.LineCollection(lines, linestyles='-', linewidths=grid_linewidth, color='grey')
    ax.add_collection(grid)
    im = plt.imshow(activities[0], animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
    if (not show_margin):
        (baseheight, basewidth) = im.get_size()
        fig.set_size_inches((basewidth * scale), (baseheight * scale), forward=True)
    i = {'index': 0}

    def updatefig(*args):
        i['index'] += 1
        if (i['index'] == len(activities)):
            i['index'] = 0
        im.set_array(activities[i['index']])
        if with_timestep:
            title_text.set_text(('timestep: %s' % (i['index'] + 1)))
        return (im, grid, title_text)
    ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=blit, save_count=len(activities))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer='imagemagick')
    plt.show()
