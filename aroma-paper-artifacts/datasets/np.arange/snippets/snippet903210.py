from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def _plot_patch_data(self, ax, data, name, mapping, borders, tick_style, x_padding=0, y_padding=0, tri_padding=0):
    "Plot data represented as patches on CoMut plot\n\n        Params:\n        -----------\n        ax: axis object\n            Axis object on which to draw the graph.\n\n        data: pandas dataframe\n            Parsed dataframe from _parse_categorical_data\n\n        name: str\n            Name of the plot to store in axes dictionary.\n\n        mapping: dict\n            mapping from add_categorical_data\n\n        borders: list-like\n            borders from add_categorical_data\n\n        x_padding: float, default=0\n            x_padding from plot_comut\n\n        y_padding: float, default=0\n            y_padding from plot_comut\n\n        tri_padding: float, default=0\n            tri_padding from plot_comut\n\n        tick_style: str, default='normal', 'italic', 'oblique'\n            Tick style to be used for the y axis ticks (category names).\n\n        Returns:\n        -------\n        ax: axis object\n            Axis object on which the plot is drawn."
    (height, width) = ((1 - (2 * y_padding)), (1 - (2 * x_padding)))
    unique_labels = set()
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            (x_base, y_base) = ((j + x_padding), (i + y_padding))
            cell_tuple = tuple(data.iloc[(i, j)])
            box_borders = [value for value in cell_tuple if (value in borders)]
            cell_tuple = [value for value in cell_tuple if (value not in borders)]
            num_values = len(cell_tuple)
            if ('Not Available' in cell_tuple):
                if (len(cell_tuple) > 1):
                    raise ValueError('Not Available must be a value by itself')
                patch_options = mapping['Not Available']
                rect = patches.Rectangle((x_base, y_base), width, height, **patch_options, label='')
                ax.add_patch(rect)
                rect.set_clip_path(rect)
                ax.plot([(x_base + (x_padding / 2)), ((x_base + width) - (x_padding / 2))], [(y_base + (y_padding / 2)), ((y_base + height) - (y_padding / 2))], color=patch_options['edgecolor'], linewidth=0.5, solid_capstyle='round')
                continue
            if (num_values != 2):
                if (num_values == 0):
                    label = 'Absent'
                    patch_options = mapping['Absent']
                elif (num_values > 2):
                    label = 'Multiple'
                    patch_options = mapping['Multiple']
                elif (num_values == 1):
                    value = cell_tuple[0]
                    label = value
                    patch_options = mapping[value]
                plot_label = (label if (label not in unique_labels) else None)
                unique_labels.add(label)
                rect = patches.Rectangle((x_base, y_base), width, height, **patch_options, label=plot_label)
                ax.add_patch(rect)
            else:
                (alt_1, alt_2) = cell_tuple
                alt_1_label = (alt_1 if (alt_1 not in unique_labels) else None)
                unique_labels.add(alt_1)
                alt_2_label = (alt_2 if (alt_2 not in unique_labels) else None)
                unique_labels.add(alt_2)
                patch_options_1 = mapping[alt_1]
                patch_options_2 = mapping[alt_2]
                (tri_1, tri_2) = self._get_triangles(x_base, y_base, tri_padding, height, width)
                tri_1_patch = patches.Polygon(tri_1, label=alt_1_label, **patch_options_1)
                tri_2_patch = patches.Polygon(tri_2, label=alt_2_label, **patch_options_2)
                ax.add_patch(tri_1_patch)
                ax.add_patch(tri_2_patch)
            for value in box_borders:
                border_options = mapping[value]
                rect = patches.Rectangle((x_base, y_base), width, height, **border_options, label=value)
                ax.add_patch(rect)
                rect.set_clip_path(rect)
    ax.set_ylim([0, (len(data.index) + y_padding)])
    ax.set_xlim([0, (len(data.columns) + x_padding)])
    ax.set_yticks(np.arange(0.5, (len(data.index) + 0.5)))
    ax.set_yticklabels(data.index, style=tick_style)
    ax.get_xaxis().set_visible(False)
    ax.tick_params(axis='both', which='both', bottom=False, top=False, length=0)
    for loc in ['top', 'right', 'bottom', 'left']:
        ax.spines[loc].set_visible(False)
    self.axes[name] = ax
    return ax
