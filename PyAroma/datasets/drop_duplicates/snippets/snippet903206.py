from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.offsetbox as offsetbox
import palettable
from collections import defaultdict


def add_categorical_data(self, data, name=None, category_order=None, value_order=None, mapping=None, borders=None, priority=None, tick_style='normal'):
    'Add categorical data to the CoMut object.\n\n        Params:\n        -------\n        data: pandas dataframe\n            A tidy dataframe containing data. Required columns are\n            sample, category, and value. Other columns are ignored.\n\n            Example:\n            -------\n            sample   | category | value\n            ----------------------------\n            Sample_1 | TP53     | Missense\n            Sample_1 | Gender   | Male\n\n        name: str\n            The name of the dataset being added. Used to references axes.\n\n            Example:\n            --------\n            example_comut = comut.CoMut()\n            example_comut.add_categorical_data(data, name = \'Mutation type\')\n\n        category_order: list-like\n            Order of category to plot, from top to bottom. Only these\n            categories are plotted.\n\n            Example:\n            --------\n            example_comut = comut.CoMut()\n            example_comut.add_categorical_data(data, category_order = [\'TP53\', \'BRAF\'])\n\n        value_order: list-like\n            Order of plotting of values in a single patch, from left\n            triangle to right triangle.\n\n            Example:\n            --------\n            value_order = [\'Amp\', \'Missense\']\n\n            If Amp and Missense exist in the same category and sample, Amp\n            will be drawn as left triangle, Missense as right.\n\n        mapping: dict\n            Mapping of values to patch properties. The dict can either specify\n            only the facecolor or other patches properties.\n\n            Note:\n            -----\n            Three additional values are required to fully specify mapping:\n\n            \'Absent\', which determines the color for samples without value\n            for a name (default white).\n\n            \'Multiple\', which determines the color for samples with more than\n            two values in that category (default brown).\n\n            \'Not Available\', which determines the patch properties when a sample\'s\n            value is \'Not Available\'.\n\n        borders: list-like\n            List of values that should be plotted as borders, not patches.\n\n            Example:\n            --------\n            example_comut = comut.CoMut()\n            example_comut.add_categorical_data(data, borders = [\'LOH\'])\n\n        priority: list-like\n            Ordered list of priorities for values. The function will attempt\n            to preserve values in this list, subverting the "Multiple"\n            assignment.\n\n            Example:\n            --------\n            example_comut.add_categorical_data(data, priority = [\'Amp\'])\n\n            If Amp exists alongside two other values, it will be drawn as\n            Amp + Multiple (two triangles), instead of Multiple.\n\n        tick_style: str, default=\'normal\', \'italic\', \'oblique\'\n            Tick style to be used for the y axis ticks (category names).\n\n        Returns:\n        --------\n        None'
    req_cols = {'sample', 'category', 'value'}
    if (not req_cols.issubset(data.columns)):
        missing_cols = (req_cols - set(data.columns))
        msg = ', '.join(list(missing_cols))
        raise ValueError('Data missing required columns: {}'.format(msg))
    samples = list(data['sample'].drop_duplicates())
    if (self.samples is None):
        self.samples = samples
    else:
        self._check_samples(samples)
    if (name is None):
        name = len(self._plots)
    if (borders is None):
        borders = []
    if (priority is None):
        priority = []
    if (value_order is None):
        value_order = []
    if (category_order is None):
        category_order = list(data['category'].drop_duplicates())
    unique_values = set(data['value'])
    if (mapping is None):
        mapping = {}
        for value in borders:
            mapping[value] = {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1}
        non_border = [val for val in unique_values if (val not in borders)]
        default_cmap = self._get_default_categorical_cmap(len(non_border))
        for (i, value) in enumerate(unique_values):
            mapping[value] = {'facecolor': default_cmap[i]}
        mapping['Absent'] = {'facecolor': 'white'}
        mapping['Multiple'] = {'facecolor': palettable.colorbrewer.qualitative.Set1_7.mpl_colors[6]}
        mapping['Not Available'] = {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1}
    elif isinstance(mapping, dict):
        mapping = mapping.copy()
        if ('Not Available' not in mapping):
            mapping['Not Available'] = {'facecolor': 'none', 'edgecolor': 'black', 'linewidth': 1}
        if ('Absent' not in mapping):
            mapping['Absent'] = {'facecolor': 'white'}
        if ('Multiple' not in mapping):
            mapping['Multiple'] = {'facecolor': palettable.colorbrewer.qualitative.Set1_7.mpl_colors[6]}
        if (not unique_values.issubset(mapping.keys())):
            missing_cats = (unique_values - set(mapping.keys()))
            raise ValueError('Categories present in dataframe {} are missing from mapping'.format(missing_cats))
        for (key, value) in mapping.items():
            if (not isinstance(value, dict)):
                if (key in borders):
                    mapping[key] = {'facecolor': 'none', 'edgecolor': value}
                else:
                    mapping[key] = {'facecolor': value}
        for border in borders:
            if (mapping[border]['facecolor'] != 'none'):
                raise ValueError("Border category {} must have facecolor = 'none'".format(border))
    else:
        raise ValueError('Invalid mapping. Mapping must be a dict.')
    parsed_data = self._parse_categorical_data(data, category_order, self.samples, value_order, priority)
    plot_data = {'data': parsed_data, 'patches_options': mapping, 'tick_style': tick_style, 'borders': borders, 'type': 'categorical'}
    self._plots[name] = plot_data
    return None
