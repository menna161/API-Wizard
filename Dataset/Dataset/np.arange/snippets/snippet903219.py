from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def plot_comut(self, fig=None, spec=None, x_padding=0, y_padding=0, tri_padding=0, heights=None, hspace=0.2, subplot_hspace=None, widths=None, wspace=0.2, structure=None, figsize=(10, 6)):
    "plot the CoMut object\n\n        Params:\n        -----------\n        fig: `~.figure.Figure`\n            The figure on which to create the CoMut plot. If no fig\n            is passed, it will be created.\n\n        spec: gridspec\n            The gridspec on which to create the CoMut plot. If no spec\n            is passed, one will be created.\n\n        x_padding, y_padding: float, optional (default 0)\n            The space between patches in the CoMut plot in the x and y\n            direction.\n\n        tri_padding: float\n            If there are two values for a sample in a category, the spacing\n            between the triangles that represent each value.\n\n        heights: dict\n            The relative heights of all the plots. Dict should have keys as\n            plot names and values as relative height.\n\n            Height values for each plot type default to the following:\n                Number of categories for categorical data\n                1 for continuous data\n                3 for bar plots\n                1 for sample indicator\n\n            Example:\n            --------\n            heights = {'plot1': 3, 'plot2': 5, 'plot3': 7}\n            CoMut.plot_comut(heights=heights)\n\n        hspace: float, default 0.2\n            The distance between different plots in the CoMut plot.\n\n        widths: list-like\n            The relative widths of plots in the x direction. Valid only\n            if side bar plots are added. Defaults to 5 for the central CoMut\n            and 1 for each side plot.\n\n            Example:\n            --------\n            widths = [0.5, 5]\n            CoMut.plot_comut(widths=heights)\n\n        wspace: float, default 0.2\n            The distance between different plots in the x-direction\n            (ie side bar plots)\n\n        structure: list-like\n            List containing desired CoMut structure. Must be provided\n            as list of lists (see example). Default structure is to place\n            each plot in its own list.\n\n            Example:\n            --------\n            # plot plot1 and plot2 in a separate subplot from plot4, don't plot\n            # plot3.\n            structure = [('plot1', 'plot2'), ('plot4')]\n            CoMut.plot_comut(structure=structure)\n\n        sublot_hspace: float\n            The distance between plots in a subplot. The scale for\n            subplot_hspace and hspace are not the same.\n\n        figsize (float, float), optional, default: (10,6)\n            width, height of CoMut figure in inches. Only valid if fig argument\n            is None.\n\n        Returns:\n        -------\n        self: CoMut object\n            CoMut object with updated axes and figure attributes.\n\n        Example\n        --------\n        # create CoMut object\n        ex_comut = comut.CoMut()\n\n        # add mutation data\n        ex_comut.add_categorical_data(mutation_data, name='mutation')\n\n        # add clinical data\n        ex_comut.add_categorical_data(tumor_stage, name='tumor_stage')\n        ex_comut.add_continuous_data(purity_data, name='purity')\n\n        # plot CoMut data\n        ex_comut.plot_comut()\n\n        # ex_comut.axes will be a dictionary with keys 'mutation', 'tumor_stage',\n        # and 'purity', with values equal to the plotted axes."
    if (structure is None):
        structure = [[plot] for plot in self._plots]
    if (heights is None):
        heights = {}
    num_subplots = len(structure)
    heights = self._get_height_spec(structure, heights)
    plot_heights = [sum(height) for height in heights][::(- 1)]
    if (fig is None):
        fig = plt.figure(figsize=figsize)
    if (widths is None):
        (widths, comut_idx) = self._get_default_widths_and_comut_loc()
    else:
        (_, comut_idx) = self._get_default_widths_and_comut_loc()
    num_cols = len(widths)
    if (spec is None):
        spec = gridspec.GridSpec(ncols=num_cols, nrows=num_subplots, figure=fig, height_ratios=plot_heights, width_ratios=widths, hspace=hspace, wspace=wspace)
    else:
        spec = gridspec.GridSpecFromSubplotSpec(ncols=num_cols, nrows=num_subplots, height_ratios=plot_heights, width_ratios=widths, hspace=hspace, wspace=wspace, subplot_spec=spec)
    for (i, (plot, height)) in enumerate(zip(structure, heights)):
        if (i == 0):
            sharex = None
            first_plot = plot[0]
        else:
            sharex = self.axes[first_plot]
        if (len(plot) == 1):
            plot_name = plot[0]
            ax = fig.add_subplot(spec[(((num_subplots - i) - 1), comut_idx)], sharex=sharex)
            ax = self._plot_data_on_axis(ax=ax, plot_name=plot_name, x_padding=x_padding, y_padding=y_padding, tri_padding=tri_padding)
            side_plots = self._side_plots[plot_name]
            (left_idx, right_idx) = (1, 1)
            for (side_name, side_plot) in side_plots.items():
                position = side_plot['position']
                if (position == 'left'):
                    sideplot_idx = (comut_idx - left_idx)
                    left_idx += 1
                elif (position == 'right'):
                    sideplot_idx = (comut_idx + right_idx)
                    right_idx += 1
                side_ax = fig.add_subplot(spec[(((num_subplots - i) - 1), sideplot_idx)])
                side_ax = self._plot_side_bar_data(side_ax, side_name, y_padding=y_padding, **side_plot)
                side_ax.set_ylim(ax.get_ylim())
        else:
            num_plots = len(plot)
            height = height[::(- 1)]
            subplot_spec = gridspec.GridSpecFromSubplotSpec(ncols=1, nrows=num_plots, hspace=subplot_hspace, subplot_spec=spec[(((num_subplots - i) - 1), comut_idx)], height_ratios=height)
            for (j, plot_name) in enumerate(plot):
                ax = fig.add_subplot(subplot_spec[(((num_plots - j) - 1), 0)], sharex=sharex)
                ax = self._plot_data_on_axis(ax=ax, plot_name=plot_name, x_padding=x_padding, y_padding=y_padding, tri_padding=tri_padding)
                if self._side_plots[plot_name]:
                    raise ValueError('Side bar plot for {} cannot be created. Plots within a subplot cannot have a side plot.'.format(plot_name))
    self.axes[first_plot].set_xticks(np.arange(0.5, (len(self.samples) + 0.5)))
    self.axes[first_plot].set_xticklabels(self.samples, rotation=90)
    self.axes[first_plot].get_xaxis().set_visible(True)
    self.axes[first_plot].tick_params(axis='x', which='both', bottom=False, length=0)
    self.figure = fig
    return self
