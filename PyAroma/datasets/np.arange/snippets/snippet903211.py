from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def _plot_bar_data(self, ax, data, name, mapping, stacked, ylabel, bar_kwargs):
    'Plot bar plot on CoMut plot\n\n        Params:\n        -----------\n        ax: axis object\n            axis object on which to draw the graph.\n\n        data: pandas Dataframe\n            Dataframe from add_bar_data\n\n        name: str\n            name from add_bar_data\n\n        mapping: dict\n            mapping from add_bar_data\n\n        stacked: bool\n            stacked from add_bar_data\n\n        ylabel: str\n            ylabel from add_bar_data\n\n        bar_kwargs: dict\n            bar_kwargs from add_bar_data\n\n        Returns:\n        -------\n        ax: axis object\n            Axis object on which the plot is drawn'
    x_range = np.arange(0.5, len(data.index))
    if stacked:
        cum_bar_df = np.cumsum(data, axis=1)
        for i in range(len(cum_bar_df.columns)):
            column = cum_bar_df.columns[i]
            color = mapping[column]
            if (i == 0):
                bottom = None
                bar_data = cum_bar_df.loc[(:, column)]
            else:
                prev_column = cum_bar_df.columns[(i - 1)]
                bar_data = (cum_bar_df.loc[(:, column)] - cum_bar_df.loc[(:, prev_column)])
                bottom = cum_bar_df.loc[(:, prev_column)]
            ax.bar(x_range, bar_data, align='center', color=color, bottom=bottom, label=column, **bar_kwargs)
    else:
        color = mapping[data.columns[0]]
        ax.bar(x_range, data.iloc[(:, 0)], align='center', color=color, label='', **bar_kwargs)
    ax.get_xaxis().set_visible(False)
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_visible(False)
    ax.set_ylabel(ylabel)
    self.axes[name] = ax
    return ax
