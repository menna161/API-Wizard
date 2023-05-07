from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def _plot_side_bar_data(self, ax, name, data, mapping, position, stacked, xlabel, y_padding, bar_kwargs):
    'Plot side bar plot on CoMut plot\n\n        Params:\n        -----------\n        ax: axis object\n            axis object on which to draw the graph.\n\n        data: pandas Dataframe\n            data from add_side_bar_data\n\n        name: str\n            name from add_side_bar_data\n\n        mapping: dict\n            mapping from add_side_bar_data\n\n        position: str, left or right\n            position from add_side_bar_data\n\n        stacked: bool\n            stacked from add_side_bar_data\n\n        xlabel: str\n            xlabel from add_side_bar_data\n\n        y_padding: float\n            y_padding from plot_comut\n\n        bar_kwargs: dict\n            bar_kwargs from add_side_bar_data\n\n        Returns:\n        -------\n        ax: axis object\n            The axis object on which the plot is drawn.'
    y_range = np.arange(0.5, len(data.index))
    if ('height' not in bar_kwargs):
        bar_kwargs['height'] = (1 - (2 * y_padding))
    if stacked:
        cum_bar_df = np.cumsum(data, axis=1)
        for i in range(len(cum_bar_df.columns)):
            column = cum_bar_df.columns[i]
            color = mapping[column]
            if (i == 0):
                left = None
                bar_data = cum_bar_df.loc[(:, column)]
            else:
                prev_column = cum_bar_df.columns[(i - 1)]
                bar_data = (cum_bar_df.loc[(:, column)] - cum_bar_df.loc[(:, prev_column)])
                left = cum_bar_df.loc[(:, prev_column)]
            ax.barh(y_range, bar_data, align='center', color=color, left=left, label=column, **bar_kwargs)
    else:
        color = mapping[data.columns[0]]
        ax.barh(y_range, data.iloc[(:, 0)], align='center', color=color, **bar_kwargs)
    if (position == 'left'):
        xlim = ax.get_xlim()
        ax.set_xlim(xlim[::(- 1)])
    ax.set_yticklabels([])
    ax.tick_params(axis='y', which='both', length=0)
    for loc in ['top', 'right', 'left']:
        ax.spines[loc].set_visible(False)
    ax.set_xlabel(xlabel)
    self.axes[name] = ax
    return ax
